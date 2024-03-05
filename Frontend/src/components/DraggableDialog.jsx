import React, { useState } from 'react';
import Draggable from 'react-draggable';
import { Dialog, DialogContent, TextField, Button, Typography, DialogTitle } from '@mui/material';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import { toast } from 'react-toastify';


function PaperComponent(props) {
    return (
        <Draggable handle=".draggable-dialog-handle" cancel={'[class*="MuiDialogContent-root"]'}>
            <Paper {...props} />
        </Draggable>
    );
}

export default function DraggableDialog({ open, onClose, post, onSave }) {
    const [title, setTitle] = useState(post ? post.title : '');
    const [description, setDescription] = useState(post ? post.description : '');
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!title.trim()) {
            toast.error('Title is required.');
            return;
        }
        if (!file) {
            toast.error('Image is required.');
            return;
        }

        const formData = new FormData();
        const user = JSON.parse(localStorage.getItem('user'));
        formData.append('username', user.username);
        formData.append('title', title);
        formData.append('description', description);
        formData.append('Image', file);

        console.log('user', user.username);
        console.log('title', title);
        console.log('description', description);

        try {
            const base_url = import.meta.env.VITE_BASE_URL; // Make sure your base URL is correctly defined in your environment variables
            const response = await axios.post(`${base_url}/upload-post?username=${user.username}&title=${title}&description=${description}`, formData);
            const newPost = response.data;
            if (onSave) {
                onSave(newPost);
            }
            onClose(); // Close the dialog on success
            alert('Post uploaded successfully');
        } catch (error) {
            console.error('Error submitting the form:', error);
            alert('Failed to upload the post.');
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            PaperComponent={PaperComponent}
            aria-labelledby="draggable-dialog-title"
        >
            <DialogTitle style={{ cursor: 'move' }} className="draggable-dialog-handle">
                Upload a new post:
            </DialogTitle>
            <DialogContent dividers>
                <form onSubmit={handleSubmit}>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="title"
                        label="Title (required)"
                        type="text"
                        fullWidth
                        variant="standard"
                        required
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="description"
                        label="Description (optional)"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={description || ''}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                    <input
                        accept="image/jpeg"
                        style={{ marginTop: '20px' }}
                        id="contained-button-file"
                        type="file"
                        onChange={handleFileChange}
                    />
                    <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
                        <Button onClick={onClose}>Cancel</Button>
                        <Button type="submit">Submit</Button>
                    </div>
                </form>
            </DialogContent>
        </Dialog>
    );
}
