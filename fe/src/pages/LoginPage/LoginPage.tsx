import { Box, Button, Typography, useTheme } from "@mui/material";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import React from "react";
import GoogleLogo from "@/assets/Google.png";
import Carousel from "react-material-ui-carousel";
import visual1 from "@/assets/visual1.jpg";
import visual2 from "@/assets/visual2.jpg";
import visual3 from "@/assets/visual3.jpg";
import visual4 from "@/assets/visual4.jpg";
import visual5 from "@/assets/visual5.jpg";

const stepFourCarousel = [visual1, visual2, visual3, visual4, visual5];

const LoginPage: React.FC = () => {
  const theme = useTheme();

  return (
    <Box>
      <Carousel
        duration={700}
        indicators={false}
        swipe={true}
        autoPlay={true}
        animation="fade"
        cycleNavigation={true}
        navButtonsAlwaysVisible={false}
        navButtonsAlwaysInvisible={false}
        sx={{ width: "100%", height: "100vh" }}
      >
        {stepFourCarousel.map((content, index) => (
          <Box
            key={index}
            component={"img"}
            src={content}
            alt="visual img"
            sx={{
              width: "100%",
              height: "100vh",
              objectFit: "cover",
              background: "rgba(255, 255, 255, 0.5)",
              filter: "brightness(50%)",
            }}
          />
        ))}
      </Carousel>

      <Box
        display={"flex"}
        flexDirection={"column"}
        justifyContent={"center"}
        gap={10}
        sx={{
          background: "white",
          position: "absolute",
          zIndex: 999,
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          boxShadow: "0px 2px 16px -4px rgba(0,0,0,0.4)",
          borderRadius: 2,
          p: 5,
          minWidth: 340,
          height: 400,
        }}
      >
        <Box
          display={"flex"}
          flexDirection={"column"}
          gap={1}
          alignItems={"center"}
        >
          <Typography
            variant="h3"
            sx={{
              fontWeight: 600,
              color: theme.palette.info.main,
            }}
          >
            TravelPicker
          </Typography>
          <Typography
            variant="body1"
            sx={{ fontWeight: 600, color: theme.palette.text.secondary }}
          >
            잊지 못할 추억을 더욱 특별하게
          </Typography>
        </Box>

        <Box flex={1} display={"flex"} gap={2} flexDirection={"column"}>
          <Button
            size="large"
            variant="outlined"
            sx={{ "&:focus": { outline: "none" } }}
            startIcon={
              <Box component={"img"} src={GoogleLogo} alt="Google Logo img" />
            }
            endIcon={<ChevronRightIcon />}
          >
            <Box sx={{ paddingRight: 2 }}>Google을 통해 로그인 하기</Box>
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
