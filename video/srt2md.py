from pathlib import Path
import sys
import subprocess


# Get directory path from command line argument
directory_path = Path(sys.argv[1])

# Check if directory exists
if not directory_path.exists():
    print("Directory does not exist.")
    sys.exit()

# Use a list comprehension to extract all files with a .srt extension
srt_files = [file for file in directory_path.glob("*.srt")]

for srt_file in srt_files:
    md_content = ""
    with open(srt_file, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            start_time, _ = lines[i+1].strip().split(' --> ')
            subtitle = lines[i+2].strip()
            # print(start_time, subtitle)
            t = start_time.split(',')[0]
            t_short = t[3:] if t.startswith('00:') else t
            md_content += f"""[({t_short})](kmtrigger://macro=1E194478-AABF-46EA-A53B-872E0554DCC2&value={t_short}) {subtitle}  \n"""
        
    md_file = (srt_file.parent / "md" / srt_file.stem).with_suffix('.md')
    with open(md_file, 'w') as md_f:
        md_f.write(md_content)


    # Convert all .md files in the directory to .pdf files using pandoc
    # pdf_file = (md_file.parent / md_file.stem).with_suffix('.pdf')
    # subprocess.run(['pandoc', '--pdf-engine=xelatex', f'--template=pandoc/template.tex', '-V', 'urlcolor=NavyBlue', str(md_file), '-o', str(pdf_file)])
    html_dir = srt_file.parent / "html"
    if not html_dir.exists():
        html_dir.mkdir()
    html_fn = (html_dir / srt_file.stem).with_suffix('.html')
    subprocess.run(['pandoc', str(md_file), '-o', str(html_fn)])
    # break
