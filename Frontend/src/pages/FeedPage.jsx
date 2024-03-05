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
    const [currentPost, setCurrentPost] = useState(null); // For edit operation
    const { searchCriteria, searchPerformed, setSearchPerformed } = useSearch();
    const local_s3_url = "https://art-gallery.s3.localhost.localstack.cloud:4566/"; // TODO: insert it into .env file

    const handleOpenDialog = (post = null) => {
        setCurrentPost(post); // `null` for new post, or the post data for editing
        setDialogOpen(true);
    };

    const handleSavePost = (newPost) => {
        setPosts([...posts, newPost]);
    };

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const baseURL = import.meta.env.VITE_BASE_URL;
                const params = {};

                // Include search criteria in the request only if they are provided
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
                    <CustomCard
                        key={post.postId}
                        username={post.username}
                        title={post.title}
                        desc={post.description}
                        imgSrc={local_s3_url + post.path_to_image}
                        date={post.insertionTime}
                        sx={{ backgroundColor: '#E0E0E0' }}
                        onClick={() => handleOpenDialog(post)} // Assuming CustomCard can handle onClick for edit
                    />
                ))}
            </Masonry>
            <CustomAddButton onClick={() => handleOpenDialog()} />
            {dialogOpen && (
                <DraggableDialog
                    open={dialogOpen}
                    onClose={() => setDialogOpen(false)}
                    post={currentPost}
                    onSave={handleSavePost}
                />
            )}
        </CustomFeedContainer>
    );
}

export default FeedPage;