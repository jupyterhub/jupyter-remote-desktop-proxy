#!/usr/bin/env python
"""
Build and push all the images we maintain
"""
import argparse
import secrets
import subprocess
from pathlib import Path

IMAGES = {
    "base": None,
    "qgis": "base",
}

HERE = Path(__file__).parent


def build(name: str, image_spec: str, build_args: dict, platform: str):
    """
    Build a given image with docker buildx

    Args:
        name (str): Name of image to build. Expects a subdirectory with this name to exist.
        image_spec (str): Image spec to tag this image with
        build_args (dict): Dict of build arguments to pass to the docker build
        platform (str): Parameters passed to --platform of docker buildx, to build for different
                        platforms.
    """
    print(f"Building {name} tagged {image_spec} for {platform}")
    cmd = [
        'docker',
        'buildx',
        'build',
        '--load',
        '--progress',
        'plain',
        '--platform',
        platform,
        '-t',
        image_spec,
    ]
    for key, value in build_args.items():
        cmd += ['--build-arg', f'{key}={value}']

    cmd.append(name)

    print(f"Running {' '.join(cmd)}")
    subprocess.check_call(cmd)


def get_tags(name: str, image_spec: str) -> list[str]:
    """
    Generate list of tags to tag this image with.

    Args:
        name (str): Name of image to build.
                    If there is a file named tags-generator inside this image directory,
                    it will be copied into the container, executed and each line in the
                    output will be used as a tag for this particular image. In addition,
                    the file `common-tags-generator` will also be run, and its output will
                    be treated the same way.
        image_spec (str): Built existing image to run commands in to generate tags with.

    Returns:
        list[str]: List of strings that this image should be tagged with.
    """
    # Autogenerate a container name that is unlikely to exist already
    # Lets us copy files into and run commands inside the same container
    container_name = secrets.token_hex(8)
    try:
        # Start a container with the given image running in the background
        subprocess.check_call(
            [
                'docker',
                'container',
                'run',
                '--rm',
                '--detach',
                '--name',
                container_name,
                image_spec,
            ]
        )

        # Print logs of the started container, to help debug
        subprocess.check_call(['docker', 'logs', container_name])

        # Make a list of scripts to be copied into this running container and
        # used to generate tags for this image. `common-tags-generator` is copied
        # and used for all images, and a `tags-generator` script is used if it is
        # present.
        tag_generator_scripts = [
            str(f)
            for f in [
                HERE / "common-tags-generator",
                HERE / name / "tags-generator",
            ]
            if f.exists()
        ]

        tags = set()

        for tgs in tag_generator_scripts:
            # Copy the tag generator script into the container under /tmp
            # This script is expected to be executable and run without any dependencies
            subprocess.check_call(
                [
                    'docker',
                    'container',
                    'cp',
                    str(tgs),
                    f'{container_name}:/tmp/tags-generator',
                ]
            )

            # Run the tags-generator script inside the container, treat each
            # line output to stdout as its own tag.
            tags.update(
                set(
                    subprocess.check_output(
                        [
                            'docker',
                            'container',
                            'exec',
                            container_name,
                            '/tmp/tags-generator',
                        ]
                    )
                    .decode()
                    .strip()
                    .split('\n')
                )
            )

        return tags
    finally:
        # When done, cleanup our container so it's not left running
        subprocess.check_call(['docker', 'container', 'stop', container_name])


def images_to_build(name: str, image_dependencies_graph: dict[str, str]) -> list[str]:
    """
    Generate ordered list of images to build for given image.
    """

    # We gotta build the image itself
    to_build = [name]

    # We gotta build the parent if it exists
    parent = image_dependencies_graph[name]

    # Follow the parent of the image until we reach the base image which
    # has no parent.
    while parent is not None:
        # We have reached the root of the set of images to build
        to_build.append(parent)
        parent = image_dependencies_graph[parent]

    # Reverse the list of images, so it can be built sequentially.
    to_build.reverse()
    return to_build


def get_git_head_sha() -> str:
    """
    Return short SHA of the current git checkout of this repository

    Returns:
        str: SHA of current git checkout
    """
    return (
        subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=HERE)
        .decode()
        .strip()
    )


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        '--image-prefix',
        default='quay.io/jupyter-remote-desktop-proxy/',
        help='Prefix used for tagging and building images',
    )
    argparser.add_argument(
        '--platforms', help="Platform to build this image for", default='linux/amd64'
    )
    argparser.add_argument(
        '--push', help='Push built images to docker registry', action='store_true'
    )

    argparser.add_argument(
        'image',
        help='Image to build. Leave empty to build everything',
        nargs='?',
    )

    args = argparser.parse_args()

    git_sha = get_git_head_sha()

    build_args = {"IMAGE_PREFIX": args.image_prefix}

    if args.image is None:
        # build everything!
        to_build = list(IMAGES.keys())
    else:
        # Build only specific image we have been asked for
        to_build = images_to_build(args.image, IMAGES)

    for image in to_build:
        # Base image name to build
        base_image_spec = f"{args.image_prefix}{image}"

        # All images build with a :latest tag, and child Dockerfiles
        # will inherit from the :latest tag
        latest_image_spec = f"{base_image_spec}:latest"

        build(image, latest_image_spec, build_args, args.platforms)

        tags = get_tags(image, latest_image_spec)

        # Tag with current git sha
        tags.add(git_sha)

        # Tag with :latest as well. Without this, :latest is not pushed
        tags.add("latest")

        for t in tags:
            # Make all additional tags generated for this image
            image_spec = f"{base_image_spec}:{t}"
            subprocess.check_call(
                ['docker', 'image', 'tag', latest_image_spec, image_spec]
            )
            print(f'Tagged {latest_image_spec} -> {image_spec}')

            if args.push:
                subprocess.check_call(['docker', 'image', 'push', image_spec])
                print(f'Pushed {image_spec}')


main()
