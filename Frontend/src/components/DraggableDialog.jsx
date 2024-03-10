import React, { useEffect, useState } from 'react';
import Draggable from 'react-draggable';
import { Dialog, DialogContent, TextField, Button, DialogTitle, Box, IconButton, Paper, CircularProgress } from '@mui/material';
import axios from 'axios';
import { toast } from 'react-toastify';
import CloseIcon from '@mui/icons-material/Close';

function PaperComponent(props) {
    return (
        <Draggable handle=".draggable-dialog-handle" cancel={'[class*="MuiDialogContent-root"]'}>
            <Paper {...props} />
        </Draggable>
    );
}

export default function DraggableDialog({ open, onClose, post, onSave, isEditMode = false, localS3Url }) {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [pathToImage, setPathToImage] = useState('');
    const [imagePreview, setImagePreview] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isEditMode && post) {
            setTitle(post.title);
            setDescription(post.description || '');
            setPathToImage(post.path_to_image);
            setImagePreview(`${localS3Url}${post.path_to_image}?${new Date().getTime()}`);
        } else {
            resetForm();
        }
    }, [post, isEditMode, localS3Url]);

    const resetForm = () => {
        setTitle('');
        setDescription('');
        setPathToImage('');
        setImagePreview('');
        setFile(null);
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFile(file);
            setImagePreview(URL.createObjectURL(file));
        }
    };

    const removeSelectedImage = () => {
        setFile(null);
        setImagePreview('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        if (!isEditMode && !file) {
            toast.error('Please select an image to upload.', { autoClose: 3000, closeOnClick: true });
            setLoading(false);
            return;
        }

        const formData = new FormData();
        let hasFile = false;
        if (file) {
            formData.append('Image', file);
            hasFile = true;
        }
        // Base URL should be defined in your environment variables or directly here
        const baseURL = import.meta.env.VITE_BASE_URL;
        const user = JSON.parse(localStorage.getItem('user'));

        let url = `${baseURL}/${isEditMode ? `update-post/${post.postId}` : 'upload-post'}`;
        let queryParams = `?username=${encodeURIComponent(user.username)}`;
        queryParams += isEditMode ? `&path_to_image=${encodeURIComponent(pathToImage)}` : '';
        queryParams += title ? `&title=${encodeURIComponent(title)}` : '';
        queryParams += description ? `&description=${encodeURIComponent(description)}` : '';

        const config = hasFile ? {
            headers: { 'Content-Type': 'multipart/form-data' },
        } : {};

        try {
            const toastId = toast.loading(`${isEditMode ? 'Updating' : 'Uploading'} post...`, { autoClose: false, closeOnClick: false });
            const response = await axios({
                method: isEditMode ? 'put' : 'post',
                url: `${url}${queryParams}`,
                data: hasFile ? formData : null, // Only send formData if there's a file
                ...config,
            });
            toast.dismiss(toastId);
            toast.success(`Post ${isEditMode ? 'updated' : 'uploaded'} successfully!`, { autoClose: 3000, closeOnClick: true });
            onSave(response.data);
            setImagePreview(file ? URL.createObjectURL(file) : `${localS3Url}${response.data.path_to_image}`);
        } catch (error) {
            console.error(`Error ${isEditMode ? 'updating' : 'uploading'} post:`, error);
            toast.error(`Failed to ${isEditMode ? 'update' : 'upload'} post.`, { autoClose: 3000, closeOnClick: true });
        } finally {
            setLoading(false);
            onClose();
        }
    };


    return (
        <Dialog open={open} onClose={onClose} PaperComponent={PaperComponent} aria-labelledby="draggable-dialog-title">
            <DialogTitle style={{ cursor: 'move' }} className="draggable-dialog-handle">
                {isEditMode ? 'Edit Post' : 'Upload a New Post'}
            </DialogTitle>
            <DialogContent dividers>
                <form onSubmit={handleSubmit}>
                    <TextField autoFocus margin="dense" id="title" label="Title (required)" type="text" fullWidth variant="standard" required value={title} onChange={(e) => setTitle(e.target.value)} />
                    <TextField margin="dense" id="description" label="Description (optional)" type="text" fullWidth variant="standard" value={description} onChange={(e) => setDescription(e.target.value)} />
                    {imagePreview && (
                        <Box mt={2} textAlign="center">
                            <img src={imagePreview} alt="Preview" style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain' }} />
                            <IconButton onClick={removeSelectedImage} aria-label="remove image">
                                <CloseIcon />
                            </IconButton>
                        </Box>
                    )}
                    <Button variant="contained" component="label" fullWidth sx={{ mt: 2 }}>
                        Upload Image
                        <input type="file" hidden accept="image/*" onChange={handleFileChange} />
                    </Button>
                    <Box mt={2} display="flex" justifyContent="flex-end">
                        <Button onClick={onClose} style={{ marginRight: '8px' }}>Cancel</Button>
                        <Button type="submit" variant="contained" disabled={loading}>
                            {loading ? <CircularProgress size={24} /> : 'Submit'}
                        </Button>
                    </Box>
                </form>
            </DialogContent>
        </Dialog>
    );
}