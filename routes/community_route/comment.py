from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Comment, db

class CommentResource(Resource):
    @jwt_required()
    def get(self, postId):
        """Get all comments for a specific post."""
        comments = Comment.query.filter_by(postId=postId).all()
        return {
            "data": [
                {
                    "commentId": c.commentId,
                    "content": c.content,
                    "createdAt": c.createdAt.isoformat(),
                    "postId": c.postId,
                    "userId": c.userId,
                } for c in comments
            ]
        }, 200

    @jwt_required()
    def post(self, postId):
        """Create a new comment for a specific post."""
        user_identity = get_jwt_identity()
        userId = int(user_identity["userId"])

        data = request.json
        if 'content' not in data or not data['content']:
            return {"message": "Content is required."}, 400

        new_comment = Comment(
            content=data['content'],
            postId=postId,
            userId=userId
        )

        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment created successfully.", "commentId": new_comment.commentId}, 201
    

class CommentListResource(Resource):
    @jwt_required()
    def put(self, commentId):
        """Update an existing comment."""
        data = request.json
        comment = Comment.query.get(commentId)
        
        if not comment:
            return {"message": "Comment not found."}, 404

        if 'content' in data and data['content']:
            comment.content = data['content']
        
        db.session.commit()
        return {"message": "Comment updated successfully."}, 200

    @jwt_required()
    def delete(self, commentId):
        """Delete a comment."""
        comment = Comment.query.get(commentId)
        
        if not comment:
            return {"message": "Comment not found."}, 404

        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted successfully."}, 200
