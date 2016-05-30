import os

### Templates for generating LaTeX output.

DOCUMENT=r"""
\documentclass{article}
\usepackage[margin=0.25in,landscape]{geometry}

\begin{document}
\vfil

%(triangle)s
\end{document}
"""

MINIPAGE = r"""
\hfil
\begin{minipage}{%(cm)f%(unit)s}
%(line)s
\end{minipage} 
\hfil
\par
\vfil

"""

def factgen():
   i = n = 1
   yield n  # for 0!
   while True:
      n = n * i  # for 1! and beyond
      yield n
      i = i + 1

class Pascal(object):

   def __init__(self, n = 1000):
      fact = factgen()
      self.facts = {}
      for i in range(0, n):
         self.facts[i] = fact.next() 


   def coefficient(self, k, n):
      return  self.facts[n] / (self.facts[k] * self.facts[n-k])


   def getrow(self, n):
      return [self.coefficient(k, n) for k in range(0, n+1)]
         
   def get_latex(self, nrows=21):
      body = []
      for i in range(0, 21):
         row = p.getrow(i)
         text = [r"\textbf{\texttt{\Large %d}}" % j for j in row]
         line = r" \hfil ".join(text)
         cm = (i + 1) * 1.25
         unit = "cm"
         print("i = " + str(i) + " cm = " + str(cm))
         minibody = MINIPAGE % vars()
         body.append(minibody)
      return "\n".join(body)
    

   def render_pdf(self, nrows=21):
      triangle = self.get_latex(nrows)
      with open("triangle.tex", "w") as outfile:
         outfile.write(DOCUMENT % vars())
      os.system("latexmk -C")
      os.system("latexmk -pdf triangle")
      os.system("latexmk -c")

if __name__ == '__main__':
   p = Pascal()
   p.render_pdf()
  
