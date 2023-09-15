import argparse
import hashlib
import os
import platform
import shutil
import sys
import tarfile
import textwrap
from urllib.request import HTTPError, urlopen, urlretrieve

from xml.etree import ElementTree

machine_map = {
    "x86_64": "amd64",
}


def checksum_file(path):
    """Compute the md5 checksum of a path"""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def fetch_release_info(tigervnc_archive, tigervnc_version):
    """Fetch the download url and md5 checksum from tigervnc release rss"""
    url = (
        "https://sourceforge.net/projects/tigervnc/rss"
        f"?path=/stable/{tigervnc_version}"
    )
    release_title = f'/stable/{tigervnc_version}/{tigervnc_archive}'
    print(f"Fetching md5 and download url from {url}")
    try:
        urlopen(url)
    except HTTPError as e:
        print(f"Failed to retrieve md5 and download url: {e}")
        return {}
    
    with urlopen(url) as f:
        tree = ElementTree.parse(f)
        root = tree.getroot()
        channel = root.find('channel')
        for item in channel.iterfind('item'):
            title = item.find('title')
            if title.text == release_title:
                media = item.find('{http://video.search.yahoo.com/mrss/}content')
                url = media.get('url')
                md5 = media.find('{http://video.search.yahoo.com/mrss/}hash').text
    return url, md5


def install_tigervnc(prefix, plat, tigervnc_version):
    tigervnc_path = os.path.join(prefix, "tigervnc")

    tigervnc_archive = f"tigervnc-{tigervnc_version}.{plat}.tar.gz"
    tigervnc_archive_path = os.path.join(prefix, tigervnc_archive)

    if os.path.exists(tigervnc_path):
        print(f"Tigervnc already exists at {tigervnc_path}. Remove it to re-install.")
        print("--- Done ---")
        return

    tigervnc_url, tigervnc_md5 = fetch_release_info(tigervnc_archive, tigervnc_version)

    print(f"Downloading tigervnc {tigervnc_version} from {tigervnc_url}...")
    urlretrieve(tigervnc_url, tigervnc_archive_path)

    md5 = checksum_file(tigervnc_archive_path)
    if md5 != tigervnc_md5:
        raise OSError(f"Checksum failed {md5} != {tigervnc_md5}")

    print("Extracting the archive...")
    with tarfile.open(tigervnc_archive_path, "r") as tar_ref:
        tar_ref.extractall(prefix)

    shutil.move(f"{prefix}/tigervnc-{tigervnc_version}.{plat}/usr/bin", prefix)
    shutil.move(f"{prefix}/tigervnc-{tigervnc_version}.{plat}/usr/lib64", prefix)
    shutil.move(f"{prefix}/tigervnc-{tigervnc_version}.{plat}/usr/share", prefix)

    print(f"Installed tigervnc {tigervnc_version}")
    shutil.rmtree(f"{prefix}/tigervnc-{tigervnc_version}.{plat}")
    os.unlink(tigervnc_archive_path)
    print("--- Done ---")


def main():
    # extract supported and default versions from urls
    parser = argparse.ArgumentParser(
        description="Dependency installer helper",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--output",
        dest="installation_dir",
        default="./dependencies",
        help=textwrap.dedent(
            """\
            The installation directory (absolute or relative path).
            If it doesn't exist, it will be created.
            If no directory is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )

    machine = platform.machine()
    machine = machine_map.get(machine, machine)
    default_platform = f"{sys.platform}-{machine}"

    parser.add_argument(
        "--platform",
        dest="plat",
        default=default_platform,
        help=textwrap.dedent(
            """\
            The platform to download for.
            If no platform is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )

    parser.add_argument(
        "--traefik-version",
        dest="traefik_version",
        default="2.10.1",
        help=textwrap.dedent(
            """\
            The version of traefik to download.
            If no version is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )
    if "--etcd" in sys.argv:
        sys.exit(
            "Installing etcd is no longer supported. Visit https://github.com/etcd-io/etcd/releases/"
        )
    if "--consul" in sys.argv:
        sys.exit(
            "Installing consul is no longer supported. Visit https://developer.hashicorp.com/consul/downloads"
        )

    args = parser.parse_args()
    deps_dir = args.installation_dir
    plat = args.plat
    traefik_version = args.traefik_version.lstrip("v")

    if args.traefik:
        print(
            "Specifying --traefik is deprecated and ignored. Only installing traefik is supported.",
            file=sys.stderr,
        )

    if os.path.exists(deps_dir):
        print(f"Using existing output directory {deps_dir}...")
    else:
        print(f"Creating output directory {deps_dir}...")
        os.makedirs(deps_dir)

    install_traefik(deps_dir, plat, traefik_version)


if __name__ == "__main__":
    main()