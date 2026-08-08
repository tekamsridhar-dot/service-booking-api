from fastapi import Depends, HTTPException, status
from app.dependencies import get_current_user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access required.")
    return current_user

def require_provider(current_user=Depends(get_current_user)):
    if current_user.role.lower() != "service provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Service Provider access required.")
    return current_user

def require_customer(current_user=Depends(get_current_user)):
    if current_user.role.lower() != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Customer access required.")
    return current_user
    

def require_admin_or_provider(current_user=Depends(get_current_user)):
    if current_user.role.lower() not in ["admin","service provider"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin or Service Provider access required.")
    return current_user

def require_authenticated_user(current_user=Depends(get_current_user)):
    return current_user
