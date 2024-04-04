


from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape

padding = dict(
  leftPadding=72,
  rightPadding=72,
  topPadding=72,
  bottomPadding=18)

portrait_frame = Frame(0, 0, *A4, **padding)
landscape_frame = Frame(0, 0, *landscape(A4), **padding)

def on_page(canvas, doc, pagesize=A4):
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(pagesize[0]/2, 50, str(page_num))
    canvas.drawImage('https://www.python.org/static/community_logos/python-logo.png', 0, 0)

def on_page_landscape(canvas, doc):
  return on_page(canvas, doc, pagesize=landscape(A4))

from reportlab.platypus import PageTemplate

portrait_template = PageTemplate(
  id='portrait',
  frames=portrait_frame,
  onPage=on_page,
  pagesize=A4)

landscape_template = PageTemplate(
  id='landscape',
  frames=landscape_frame,
  onPage=on_page_landscape,
  pagesize=landscape(A4))

from reportlab.platypus import BaseDocTemplate

doc = BaseDocTemplate(
  'report.pdf',
  pageTemplates=[
    portrait_template,
    landscape_template
  ]
)

import io
from reportlab.platypus import Image
from reportlab.lib.units import inch

def fig2image(f):
    buf = io.BytesIO()
    f.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    x, y = f.get_size_inches()
    return Image(buf, x * inch, y * inch)


from reportlab.platypus import Table, Paragraph
from reportlab.lib import colors

def df2table(df):
    return Table(
      [[Paragraph(col) for col in df.columns]] + df.values.tolist(),
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
      hAlign = 'LEFT')


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
    names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'plant_type']
)

plant_type_df = df.groupby('plant_type').mean()

plant_type_fig, ax = plt.subplots(dpi=300)
plant_type_df.plot.bar(rot=0, ax=ax)
plt.ylim(0, 8)
#plt.show()

scatter_matrix_fig, ax = plt.subplots(dpi=300, figsize=(7, 7))
pd.plotting.scatter_matrix(df, ax=ax)
plt.tight_layout()
#plt.show()

from reportlab.platypus import NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

story = [
      Paragraph('Iris Dataset Report', styles['Heading1']),
      Paragraph('Scatter Matrix', styles['Heading2']),
      fig2image(scatter_matrix_fig),
      Paragraph('Pairwise Correlation', styles['Heading2']),
      df2table(plant_type_df.corr()),
      NextPageTemplate('landscape'),
      PageBreak(),
      Paragraph('Mean Features by Plant Type', styles['Heading2']),
      fig2image(plant_type_fig),
      df2table(plant_type_df),

]

doc.build(story)

