import { ThemeProvider, createTheme } from "@mui/material";
import "./App.css";
import { Outlet } from "react-router-dom";

function App() {
  const defaultTheme = createTheme({
    typography: {
      fontFamily: "Pretendard Variable, Roboto, sans-serif",
    },
  });

  return (
    <ThemeProvider theme={defaultTheme}>
      <Outlet />
    </ThemeProvider>
  );
}

export default App;
