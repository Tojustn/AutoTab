import ThemeButton from "./ThemeButton.tsx";

const NavBar = () => {
  return (
    <div className="flex flex-row justify-between absolute w-full">
      <h1 className="text-4xl font-bold text-center mb-10 px-2 py-1">
        AutoTab
      </h1>
      <ThemeButton />
    </div>
  );
};

export default NavBar;
