import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Github, Sun, Moon, Menu, ChefHat } from "lucide-react";

export default function NavBar({ toggleTheme, theme }) {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const linkClasses = (path) =>
    `block hover:font-semibold cursor-pointer transition-all ${
      location.pathname === path ? "font-bold" : ""
    }`;

  return (
    <nav className="bg-gray-50 dark:bg-black border-b border-gray-200 dark:border-gray-700 font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Left side */}
          <div className="flex items-center space-x-8">
            <Link to="/" className="hover:opacity-80">
              <ChefHat size={28} className="cursor-pointer transition-all" />
            </Link>

            <div className="hidden md:flex space-x-8 text-lg">
              <Link to="/" className={linkClasses("/")}>Recipe Catalog</Link>
              <Link to="/recipes" className={linkClasses("/recipes")}>Recipes</Link>
              <Link to="/shopping-list" className={linkClasses("/shopping-list")}>Shopping List</Link>
            </div>
          </div>

          {/* Right side icons (desktop only) */}
          <div className="hidden md:flex items-center space-x-6">
            <a
              href="https://github.com/jjschirle/recipe-catalog"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:opacity-80 transition-all"
            >
              <Github size={28} className="cursor-pointer" />
            </a>
            <button
              onClick={toggleTheme}
              className={`w-16 h-8 flex items-center bg-gray-300 dark:bg-gray-600 rounded-full p-1 transition-colors`}
            >
              <div
                className={`bg-white dark:bg-black w-6 h-6 rounded-full shadow-md transform duration-150 ease-in-out ${
                  theme === "dark" ? "translate-x-8" : "translate-x-0"
                }`}
              >
                {theme === "light" ? (
                  <Moon size={18} className="mx-auto mt-[2px] text-gray-700" />
                ) : (
                  <Sun size={18} className="mx-auto mt-[2px] text-yellow-400" />
                )}
              </div>
            </button>
          </div>
          {/* Mobile menu toggle */}
          <button
            className={`md:hidden ml-2 p-1 rounded-md border transition-opacity
              ${theme === "dark" ? "border-white" : "border-black"}
              hover:opacity-80`}
            onClick={() => setIsOpen(!isOpen)}
          >
            <Menu size={26} />
          </button>
        </div>
      </div>

      {/* Mobile dropdown with smooth height animation */}
      <div
        className={`md:hidden px-4 overflow-hidden transition-all duration-300 ease-in-out
          ${isOpen ? "max-h-screen pt-4 pb-4" : "max-h-0 pt-0 pb-0"}`}
      >
        <Link
          to="/"
          className={linkClasses("/")}
          onClick={() => setIsOpen(false)}
        >
          Recipe Catalog
        </Link>
        <Link
          to="/recipes"
          className={linkClasses("/recipes")}
          onClick={() => setIsOpen(false)}
        >
          Recipes
        </Link>
        <Link
          to="/shopping-list"
          className={linkClasses("/shopping-list")}
          onClick={() => setIsOpen(false)}
        >
          Shopping List
        </Link>

        <a
          href="https://github.com/jjschirle/recipe-catalog"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:opacity-80 transition-all block mt-4"
        >
          <Github size={28} className="cursor-pointer" />
        </a>
        {/* Mobile menu toggle button with border */}
        <button
          onClick={() => {
            toggleTheme();
            setIsOpen(false);
          }}
          className={`w-16 h-8 flex items-center bg-gray-300 dark:bg-gray-600 rounded-full p-1 transition-colors mt-4`}
        >
          <div
            className={`bg-white dark:bg-black w-6 h-6 rounded-full shadow-md transform duration-150 ease-in-out ${
              theme === "dark" ? "translate-x-8" : "translate-x-0"
            }`}
          >
            {theme === "light" ? (
              <Moon size={18} className="mx-auto mt-[2px] text-gray-700" />
            ) : (
              <Sun size={18} className="mx-auto mt-[2px] text-yellow-400" />
            )}
          </div>
        </button>
      </div>
    </nav>
  );
}
