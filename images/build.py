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


def build(name: str, tag: str, build_args: dict, platform: str):
    cmd = [
        'docker',
        'buildx',
        'build',
        '--load',
        '--platform',
        platform,
        '-t',
        tag,
    ]
    for key, value in build_args.items():
        cmd += ['--build-arg', f'{key}={value}']

    cmd.append(name)
    print(cmd)

    subprocess.check_call(cmd)


def get_tags(image: str, base_image_spec: str):
    container_name = secrets.token_hex(8)
    try:
        run_cmd = [
            'docker',
            'container',
            'run',
            '--detach',
            '--name',
            container_name,
            base_image_spec,
        ]
        subprocess.check_call(run_cmd)

        subprocess.check_call(
            [
                'docker',
                'container',
                'ls',
            ]
        )

        subprocess.check_call(['docker', 'logs', container_name])

        tag_generator_scripts = [
            str(f)
            for f in [
                HERE / "common-tags-generator",
                HERE / image / "tags-generator",
            ]
            if f.exists()
        ]

        tags = set()

        for tgs in tag_generator_scripts:
            subprocess.check_call(
                [
                    'docker',
                    'container',
                    'cp',
                    str(tgs),
                    f'{container_name}:/tmp/tags-generator',
                ]
            )

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

        print(tags)
        return tags

    finally:
        subprocess.check_call(['docker', 'container', 'stop', container_name])


def images_to_build(name: str, image_dependencies_graph: dict[str, str]) -> list[str]:
    parent = image_dependencies_graph[name]

    to_build = [name]

    while parent is not None:
        # We have reached the root of the set of images to build
        to_build.append(parent)
        parent = image_dependencies_graph[parent]

    to_build.reverse()
    return to_build


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

    build_args = {"IMAGE_PREFIX": args.image_prefix}

    if args.image is None:
        # build everything
        to_build = list(IMAGES.keys())
    else:
        # Build only specific image we have been asked for
        to_build = images_to_build(args.image, IMAGES)

    for image in to_build:
        base_image_spec = f"{args.image_prefix}{image}"

        image_spec = f"{base_image_spec}:latest"

        build(image, image_spec, build_args, args.platforms)

        tags = get_tags(image, base_image_spec)

        for t in tags:
            image_spec = f"{base_image_spec}:{t}"
            subprocess.check_call(
                ['docker', 'image', 'tag', base_image_spec, image_spec]
            )
            print(f'Tagged {image_spec}')

            if args.push:
                subprocess.check_call(['docker', 'image', 'push', image_spec])
                print(f'Pushed {image_spec}')


main()
