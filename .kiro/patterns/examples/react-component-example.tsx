// Exemplo prático de componente React seguindo padrões CDD v2.0
// components/UserProfile/UserProfile.tsx

import React, { memo, useEffect, useState } from 'react';
import { useUser } from '../../hooks/useUser';
import { Button } from '../ui/Button';
import { ErrorMessage } from '../ui/ErrorMessage';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import type { UserProfileProps } from './UserProfile.types';

export const UserProfile = memo<UserProfileProps>(
  ({ userId, onEdit, onDelete, className = '', ...props }) => {
    const { user, loading, error, updateUser, deleteUser } = useUser(userId);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
      firstName: '',
      lastName: '',
      email: '',
    });

    useEffect(() => {
      if (user) {
        setFormData({
          firstName: user.firstName || '',
          lastName: user.lastName || '',
          email: user.email || '',
        });
      }
    }, [user]);

    const handleEdit = async () => {
      if (!user) return;

      try {
        await updateUser(formData);
        setIsEditing(false);
        onEdit?.(user);
      } catch (error) {
        console.error('Failed to update user:', error);
      }
    };

    const handleDelete = async () => {
      if (!user) return;

      if (window.confirm('Are you sure you want to delete this user?')) {
        try {
          await deleteUser();
          onDelete?.(user);
        } catch (error) {
          console.error('Failed to delete user:', error);
        }
      }
    };

    const handleInputChange =
      (field: keyof typeof formData) => (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
          ...prev,
          [field]: e.target.value,
        }));
      };

    if (loading) {
      return <LoadingSpinner />;
    }

    if (error) {
      return <ErrorMessage message={error} />;
    }

    if (!user) {
      return <ErrorMessage message='User not found' />;
    }

    return (
      <div className={`user-profile ${className}`} {...props}>
        <div className='user-profile__header'>
          <h2>User Profile</h2>
          <div className='user-profile__actions'>
            {!isEditing ? (
              <>
                <Button
                  variant='secondary'
                  size='small'
                  onClick={() => setIsEditing(true)}
                >
                  Edit
                </Button>
                <Button variant='danger' size='small' onClick={handleDelete}>
                  Delete
                </Button>
              </>
            ) : (
              <>
                <Button variant='primary' size='small' onClick={handleEdit}>
                  Save
                </Button>
                <Button
                  variant='secondary'
                  size='small'
                  onClick={() => setIsEditing(false)}
                >
                  Cancel
                </Button>
              </>
            )}
          </div>
        </div>

        <div className='user-profile__content'>
          {isEditing ? (
            <form className='user-profile__form'>
              <div className='form-group'>
                <label htmlFor='firstName'>First Name</label>
                <input
                  id='firstName'
                  type='text'
                  value={formData.firstName}
                  onChange={handleInputChange('firstName')}
                  className='form-input'
                />
              </div>

              <div className='form-group'>
                <label htmlFor='lastName'>Last Name</label>
                <input
                  id='lastName'
                  type='text'
                  value={formData.lastName}
                  onChange={handleInputChange('lastName')}
                  className='form-input'
                />
              </div>

              <div className='form-group'>
                <label htmlFor='email'>Email</label>
                <input
                  id='email'
                  type='email'
                  value={formData.email}
                  onChange={handleInputChange('email')}
                  className='form-input'
                />
              </div>
            </form>
          ) : (
            <div className='user-profile__info'>
              <div className='info-row'>
                <span className='info-label'>Name:</span>
                <span className='info-value'>
                  {user.firstName} {user.lastName}
                </span>
              </div>
              <div className='info-row'>
                <span className='info-label'>Email:</span>
                <span className='info-value'>{user.email}</span>
              </div>
              <div className='info-row'>
                <span className='info-label'>Status:</span>
                <span
                  className={`info-value status--${
                    user.isActive ? 'active' : 'inactive'
                  }`}
                >
                  {user.isActive ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className='info-row'>
                <span className='info-label'>Created:</span>
                <span className='info-value'>
                  {new Date(user.createdAt).toLocaleDateString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }
);

UserProfile.displayName = 'UserProfile';
