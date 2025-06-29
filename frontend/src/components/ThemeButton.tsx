import React, { useContext } from "react";
import { ThemeContext } from "../utils/ThemeContext.tsx";
import { Box, Button } from "@mui/material";

const ThemeButton = () => {
  const [theme, toggleTheme] = useContext(ThemeContext);
  return (
    <Box>
      <Button variant="contained" onClick={toggleTheme}>
        {theme === "light" ? "Dark Mode" : "Light Mode"}
      </Button>
    </Box>
  );
};

export default ThemeButton;
