### this file provide class that contain Notice subject, content, link ###

class Notice:
    subject = ""
    content = "" # html type #
    link = ""
        
    def make_script(self, posts, link):
        for post in posts:
            self.content += post + '가 등록되었습니다.\n'
        
        self.content = self.content.replace("\n", "<br>")
        
        self.link = link
    
    def make_title(self, posts, websiteName):
        self.subject = '[' + websiteName + ']' + ' '
        
        if len(posts) == 1:
            self.subject += posts[0]
        else:
            self.subject += str(len(posts)) + '개의 게시글이 등록되었습니다.'
        
    
    