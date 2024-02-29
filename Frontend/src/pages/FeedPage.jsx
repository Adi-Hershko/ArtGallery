import React from "react";
import ResponsiveAppBar from "../components/ResponsiveAppBar";
import { Box, Grid } from "@mui/material";
import CustomCard from "../components/CustomCard";
import axios from "axios";
import Masonry from '@mui/lab/Masonry';


function FeedPage() {

    const [posts, setPosts] = React.useState([]);
    const local_s3_url = "https://art-gallery.s3.localhost.localstack.cloud:4566/"; // TODO: Insert it later into .env

    React.useEffect(() => {
        const base_url = import.meta.env.VITE_BASE_URL; // Ensure you have VITE_BASE_URL in your .env
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
        <Box
            sx={{
                width: '100%',
                minHeight: '100vh',
                backgroundImage: `url('backgroundImage.webp')`,
                backgroundSize: 'fill',
                backgroundPosition: 'center',
                backgroundAttachment: 'fixed',
            }}
        >
            <ResponsiveAppBar />
            <Masonry columns={4} spacing={3} sx={
                {
                    marginX: 'auto',
                    paddingTop: '10px',
                }
            }>
                {posts.map((post) => (
                    <CustomCard
                        key={post.postId}
                        username={post.username}
                        title={post.title}
                        desc={post.description}
                        imgSrc={local_s3_url + post.path_to_image}
                        date={post.insertionTime}
                        sx={{ backgroundColor: '#E0E0E0' }}
                    />
                ))}
            </Masonry>
        </Box>
    );
}

export default FeedPage;
