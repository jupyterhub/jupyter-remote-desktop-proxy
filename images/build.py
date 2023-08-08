#!/usr/bin/env python
"""
Build and push all the images we maintain
"""
import argparse
import subprocess

IMAGES = {
    "base": None,
    "qgis": "base",
}


def build(name: str, tag: str, build_args: dict):
    cmd = [
        'docker',
        'build',
        '-t',
        tag,
    ]
    for key, value in build_args.items():
        cmd += ['--build-arg', f'{key}={value}']

    cmd.append(name)
    print(cmd)

    subprocess.check_call(cmd)


def push(tag: str):
    cmd = ['docker', 'push', tag]
    subprocess.check_call(cmd)


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
        tag = f"{args.image_prefix}{image}"

        build(image, tag, build_args)

    # Push images only after *all* images have been built. This ensures
    # we don't push a
    if args.push:
        for image in to_build:
            tag = f"{args.image_prefix}{image}"
            push(tag)


main()
