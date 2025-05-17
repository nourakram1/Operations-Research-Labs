import { useContext } from "react";
import { AppContext } from "/src/context/AppContext.jsx";

export const useAppContext = () => useContext(AppContext);
