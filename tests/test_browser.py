from os import getenv
from pathlib import Path
from shutil import which
from subprocess import check_output
from uuid import uuid4

from PIL import Image, ImageChops
from playwright.sync_api import expect

HERE = Path(__file__).absolute().parent

CONTAINER_ID = getenv("CONTAINER_ID", "test")
JUPYTER_HOST = getenv("JUPYTER_HOST", "http://localhost:8888")
JUPYTER_TOKEN = getenv("JUPYTER_TOKEN", "secret")
VNCSERVER = getenv("VNCSERVER")


def compare_screenshot(test_image):
    # Compare images by calculating the mean absolute difference
    # Images must be the same size
    # threshold: Average difference per pixel, this depends on the image type
    # e.g. for 24 bit images (8 bit RGB pixels) threshold=1 means a maximum
    # difference of 1 bit per pixel per channel
    reference = Image.open(HERE / "reference" / "desktop.png")
    threshold = 2
    if VNCSERVER == "turbovnc":
        reference = Image.open(HERE / "reference" / "desktop-turbovnc.png")
        # The TurboVNC screenshot varies a lot more than TigerVNC
        threshold = 6
    test = Image.open(test_image)

    # Absolute difference
    # Convert to RGB, alpha channel breaks ImageChops
    diff = ImageChops.difference(reference.convert("RGB"), test.convert("RGB"))
    diff_data = diff.getdata()

    m = sum(sum(px) for px in diff_data) / diff_data.size[0] / diff_data.size[1]
    assert m < threshold


# To debug this set environment variable HEADLESS=0
def test_desktop(browser):
    page = browser
    page.goto(f"{JUPYTER_HOST}/lab?token={JUPYTER_TOKEN}")
    page.wait_for_url(f"{JUPYTER_HOST}/lab")

    # JupyterLab extension icon
    expect(page.get_by_text("Desktop [↗]")).to_be_visible()
    with page.expect_popup() as page1_info:
        page.get_by_text("Desktop [↗]").click()
    page1 = page1_info.value
    page1.wait_for_url(f"{JUPYTER_HOST}/desktop/")

    expect(page1.get_by_text("Status: Connected")).to_be_visible()
    expect(page1.locator("canvas")).to_be_visible()

    # Screenshot the desktop element only
    # May take a few seconds to load
    page1.wait_for_timeout(5000)
    # Use a non temporary folder so we can check it manually if necessary
    screenshot = Path("screenshots") / "desktop.png"
    page1.locator("body").screenshot(path=screenshot)

    # Open clipboard, enter random text, close clipboard
    clipboard_text = str(uuid4())
    page1.get_by_role("link", name="Remote Clipboard").click()
    expect(page1.locator("#clipboard-text")).to_be_visible()
    page1.locator("#clipboard-text").click()
    page1.locator("#clipboard-text").fill(clipboard_text)
    # Click outside clipboard, it should be closed
    page1.locator("canvas").click(position={"x": 969, "y": 273})
    expect(page1.locator("#clipboard-text")).not_to_be_visible()

    # Exec into container to check clipboard contents
    for engine in ["docker", "podman"]:
        if which(engine):
            break
    else:
        raise RuntimeError("Container engine not found")
    clipboard = check_output(
        [engine, "exec", "-eDISPLAY=:1", CONTAINER_ID, "xclip", "-o"]
    )
    assert clipboard.decode() == clipboard_text

    compare_screenshot(screenshot)
