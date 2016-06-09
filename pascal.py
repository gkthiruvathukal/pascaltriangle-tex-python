import os
import os.path


# "Infinite" sequence of factorials

def factgen():
   i = n = 1
   yield n  # for 0!
   while True:
      n = n * i  # for 1! and beyond
      yield n
      i = i + 1

class Pascal(object):

   DOCUMENT_TEMPLATE_FILENAME = os.path.join("templates", "document.tex")
   MINIPAGE_TEMPLATE_FILENAME = os.path.join("templates", "minipage.tex")
   OUTPUT_DIR="output"
   OUTPUT_FILENAME="triangle.tex"

   def __init__(self, n = 1000):
      fact = factgen()
      self.facts = { i : fact.next() for i in range(0, n) }

   def coefficient(self, k, n):
      return  self.facts[n] / (self.facts[k] * self.facts[n-k])

   def getrow(self, n):
      return [self.coefficient(k, n) for k in range(0, n+1)]
         
   def get_latex(self, nrows=21):
      body = []
      for i in range(0, nrows):
         row = self.getrow(i)
         text = [r"\textbf{\texttt{\Large %d}}" % j for j in row]
         line = r" \hfil ".join(text)
         cm = (i + 1) * 1.25
         unit = "cm"
         print("i = " + str(i) + " cm = " + str(cm))
         minipage = self.load_file(Pascal.MINIPAGE_TEMPLATE_FILENAME)
         body.append(minipage % vars())
      return "\n".join(body)
    

   def load_file(self, filename):
      with open(filename) as f:
         return f.read()

   def render_pdf(self, nrows=21):
      triangle = self.get_latex(nrows)
      document = self.load_file(Pascal.DOCUMENT_TEMPLATE_FILENAME)
      if not os.path.exists(Pascal.OUTPUT_DIR): os.makedirs(Pascal.OUTPUT_DIR)
      output_path = os.path.join(Pascal.OUTPUT_DIR, Pascal.OUTPUT_FILENAME)
      with open(output_path, "w") as outfile:
         outfile.write(document % vars())
      output_dir_option = "-output-directory=%s" % Pascal.OUTPUT_DIR
      os.system("latexmk -pdf %(output_dir_option)s %(output_path)s" % vars())
      os.system("latexmk -c %(output_dir_option)s %(output_path)s" % vars())

if __name__ == '__main__':
   p = Pascal()
   p.render_pdf()
  
