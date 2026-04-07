#!/usr/bin/env python3
"""
Measure resume page count and fill percentage.
Usage: python3 measure_resume.py <generator_script.py>
Output: pages,fill_pct (e.g. "1,94")
"""

import sys
import os
import importlib.util
import tempfile

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 measure_resume.py <script.py>")
        sys.exit(1)

    script_path = os.path.abspath(sys.argv[1])
    script_dir = os.path.dirname(script_path)
    module_name = os.path.splitext(os.path.basename(script_path))[0]

    # Add script dir to path
    sys.path.insert(0, script_dir)

    # Suppress os.makedirs (output dir may not exist in validation context)
    _real_makedirs = os.makedirs
    os.makedirs = lambda *a, **kw: None

    # Import the generator module
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    os.makedirs = _real_makedirs

    if not hasattr(mod, 'generate_resume'):
        print("-1,-1")
        sys.exit(0)

    # Step 1: Build PDF to temp file and count pages
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
    try:
        mod.generate_resume(temp_pdf)

        with open(temp_pdf, 'rb') as f:
            pdf_bytes = f.read()
        total = pdf_bytes.count(b'/Type /Page')
        trees = pdf_bytes.count(b'/Type /Pages')
        pages = total - trees
    except Exception as e:
        print(f"-1,-1", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            os.unlink(temp_pdf)
        except OSError:
            pass

    # Step 2: Measure fill by capturing story and computing content height
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import BaseDocTemplate

    PW, PH = letter
    MARGIN_LR = getattr(mod, 'MARGIN_LR', 27)
    MARGIN_TB = getattr(mod, 'MARGIN_TB', 20)
    frame_w = PW - 2 * MARGIN_LR
    frame_h = PH - 2 * MARGIN_TB

    # Monkey-patch build to capture the story
    captured = []
    _orig_build = BaseDocTemplate.build

    def _capture_build(self, story, **kw):
        captured.extend(story)

    BaseDocTemplate.build = _capture_build
    try:
        os.makedirs = lambda *a, **kw: None
        mod.generate_resume(temp_pdf)
    except Exception:
        pass
    finally:
        BaseDocTemplate.build = _orig_build
        os.makedirs = _real_makedirs
        try:
            os.unlink(temp_pdf)
        except OSError:
            pass

    # Sum content heights
    total_h = 0.0
    for item in captured:
        try:
            w, h = item.wrap(frame_w, frame_h)
            total_h += h
            # spaceBefore/spaceAfter are added by the frame layout engine
            sb = getattr(item, 'spaceBefore', 0) or 0
            sa = getattr(item, 'spaceAfter', 0) or 0
            if sb == 0 and hasattr(item, 'style'):
                sb = getattr(item.style, 'spaceBefore', 0) or 0
            if sa == 0 and hasattr(item, 'style'):
                sa = getattr(item.style, 'spaceAfter', 0) or 0
            total_h += sb + sa
        except Exception:
            pass

    fill_pct = int(total_h / frame_h * 100) if frame_h > 0 else -1
    print(f"{pages},{fill_pct}")


if __name__ == "__main__":
    main()
