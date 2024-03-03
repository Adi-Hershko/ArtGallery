import React from "react";
import ResponsiveAppBar from "../components/ResponsiveAppBar";
import CustomCard from "../components/CustomCard";
import axios from "axios";
import Masonry from '@mui/lab/Masonry';
import CustomAddButton from "../components/CustomAddButton";
import CustomFeedContainer from "../components/CustomFeedContainer";
import DraggableDialog from "../components/DraggableDialog";

function FeedPage() {
    const [posts, setPosts] = React.useState([]);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [currentPost, setCurrentPost] = React.useState(null); // For edit operation
    const local_s3_url = "https://art-gallery.s3.localhost.localstack.cloud:4566/";

    const handleOpenDialog = (post = null) => {
        setCurrentPost(post); // `null` for new post, or the post data for editing
        setDialogOpen(true);
    };

    React.useEffect(() => {
        const base_url = import.meta.env.VITE_BASE_URL;
        const api_url = `${base_url}/posts`;

        axios.get(api_url)
            .then((res) => {
                setPosts(res.data);
            })
            .catch((error) => {
                console.error(error);
            });
    }, []);

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
                    post={currentPost} // Pass `null` for new post, or the post data for editing
                    onSave={(newData) => {
                        // Handle save operation (either create or update)
                        setDialogOpen(false);
                        if (currentPost) {
                            // Update logic
                        } else {
                            // Add logic
                            setPosts([...posts, newData]); // Example for add
                        }
                    }}
                />
            )}
        </CustomFeedContainer>
    );
}

export default FeedPage;
