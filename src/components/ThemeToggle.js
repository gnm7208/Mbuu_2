import { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";

export default function ThemeToggle() {
  const { theme, setTheme } = useContext(ThemeContext);
  return (
    <button className="btn" onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
      {theme === "light" ? "Dark" : "Light"} mode
    </button>
  );
}
