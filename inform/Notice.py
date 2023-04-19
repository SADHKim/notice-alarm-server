### this file provide class that contain Notice subject, content, link ###

class Notice:
    subject = ""
    content = "" # html type #
    link = ""
        
    def make_script(self, content, link):
        self.content = content
        self.content = self.content.replace("\n", "<br>")
        
        self.link = link
    
    def make_title(self, subject, websiteName):
        self.subject = '[' + websiteName + ']' + ' ' + subject
        
    
    