class InsertArticleError(Exception):
    pass

class AuthorNotFoundError(Exception):
    pass

class ArticleUpdatingError(Exception):
    pass

class ReturnedArticlesError(Exception):
    pass

class ReturnedArticlesByAuthorError(Exception):
    pass

class ReturnedArticlesByIdError(Exception):
    pass

class DeleteArticleError(Exception):
    pass

class DeleteArticleByIdError(Exception):
    pass

class UserExistsError(Exception):
    pass

class LoginFailedError(Exception):
    pass
