class BlogData :
    def __init__(self) :
        self.articles = []
        
    def article_count(self) :
        return len(self.articles)
    
    def comment_count(self) :
        comment_counts = map(lambda a: len(a.comments), self.articles)
        return sum(comment_counts)
    
