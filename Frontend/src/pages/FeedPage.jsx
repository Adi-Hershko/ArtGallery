import React, { useEffect, useState } from "react";
import ResponsiveAppBar from "../components/ResponsiveAppBar";
import CustomCard from "../components/CustomCard";
import axios from "axios";
import Masonry from '@mui/lab/Masonry';
import CustomAddButton from "../components/CustomAddButton";
import CustomFeedContainer from "../components/CustomFeedContainer";
import DraggableDialog from "../components/DraggableDialog";
import { useSearch } from "../contexts/SearchContext";
import { toast } from "react-toastify";

function FeedPage() {
    const [posts, setPosts] = useState([]);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [currentPost, setCurrentPost] = useState(null);
    const { searchCriteria, searchPerformed, setSearchPerformed } = useSearch();
    const [isEditMode, setIsEditMode] = useState(false);
    const local_s3_url = "https://art-gallery.s3.localhost.localstack.cloud:4566/"; // TODO: insert it into .env file

    const handleOpenDialog = (post = null) => {
        setCurrentPost(post);
        setIsEditMode(!!post);
        setDialogOpen(true);
    };

    const handleSavePost = (savedPost) => {
        if (isEditMode) {
            // Update the posts array with the updated post
            setPosts(posts.map(post => post.postId === savedPost.postId ? savedPost : post));
            // Update the currentPost if the image has changed
            if (savedPost.path_to_image !== currentPost.path_to_image) {
                setCurrentPost(prevPost => ({ ...prevPost, path_to_image: savedPost.path_to_image }));
            }
        } else {
            // Add the newly saved post to the posts array
            setPosts(prevPosts => [...prevPosts, savedPost]);
        }
    };


    const handleEditPost = (postId) => {
        const postToEdit = posts.find((post) => post.postId === postId);
        if (postToEdit) {
            setCurrentPost(postToEdit);
            setIsEditMode(true);
            setDialogOpen(true);
        } else {
            console.error("Post not found for edit:", postId);
        }
    };

    const handleDeletePost = async (postId) => {
        try {
            const baseURL = import.meta.env.VITE_BASE_URL;
            await axios.delete(`${baseURL}/delete-post/${postId}`);
            const updatedPosts = posts.filter(post => post.postId !== postId);
            setPosts(updatedPosts);
            toast.success('Post deleted successfully!', {
                position: "bottom-left",
                autoClose: 2000,
            });
        } catch (error) {
            console.error(error);
            toast.error('Failed to delete post', {
                position: "bottom-left",
                autoClose: 2000,
            });
        }
    };

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const baseURL = import.meta.env.VITE_BASE_URL;
                const params = {};

                if (searchCriteria.title) params.title = searchCriteria.title;
                if (searchCriteria.username) params.username = searchCriteria.username;

                const response = await axios.get(`${baseURL}/posts`, { params });
                setPosts(response.data);

                if (response.data.length > 0 && searchPerformed) {
                    toast.success(`${response.data.length} posts found!`, {
                        position: "bottom-left",
                        autoClose: 2000,
                    });
                } else if (searchPerformed) {
                    toast.warn('No posts found!', {
                        position: "bottom-left",
                        autoClose: 2000,
                    });
                }
            } catch (error) {
                console.error(error);
                toast.error('Failed to fetch posts', {
                    position: "bottom-left",
                    autoClose: 2000,
                });
            }
        };

        fetchPosts();
        return () => setSearchPerformed(false);
    }, [searchCriteria, setSearchPerformed, searchPerformed]);

    return (
        <CustomFeedContainer>
            <ResponsiveAppBar />
            <Masonry columns={4} spacing={3} sx={{ marginX: 'auto', paddingTop: '10px' }}>
                {posts.map((post) => (
                    post && post.postId ? ( // Ensure post and postId exist
                        <CustomCard
                            key={post.postId}
                            postId={post.postId}
                            username={post.username}
                            title={post.title}
                            desc={post.description}
                            imgSrc={local_s3_url + post.path_to_image}
                            date={post.insertionTime}
                            sx={{ backgroundColor: '#E0E0E0' }}
                            onClick={() => handleOpenDialog(post)}
                            onDelete={handleDeletePost}
                            onEdit={handleEditPost}
                        />
                    ) : null
                ))}
            </Masonry>
            <CustomAddButton onClick={() => handleOpenDialog()} />
            {dialogOpen && (
                <DraggableDialog
                    open={dialogOpen}
                    onClose={() => {
                        setDialogOpen(false);
                        setIsEditMode(false);
                        setCurrentPost(null);
                    }}
                    post={currentPost}
                    onSave={handleSavePost}
                    isEditMode={isEditMode}
                    localS3Url={local_s3_url}
                />
            )}
        </CustomFeedContainer>
    );
}

export default FeedPage;
