import {
  BookOpen,
  UsersRound,
  HomeIcon,
  TrophyIcon,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const navigationItems = [
  { icon: TrophyIcon, label: "Challenge", href: "/Challenge" },
  { icon: HomeIcon, label: "Home", href: "/Home" },
  { icon: BookOpen, label: "Library", href: "/Library" },
  { icon: UsersRound, label: "Community", href: "/Commu" },
];

interface NaviBarProps {
  activeLabel: string; // 현재 활성화된 라벨을 props로 받음
}

const NaviBar = ({ activeLabel }: NaviBarProps): JSX.Element => {
  const navigate = useNavigate();

  return (
    <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
      <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
        {navigationItems.map((item) => (
          <button
            key={item.label}
            onClick={() => navigate(item.href, { replace: true })}
            className="flex flex-col items-center w-[82px] h-[75px] bg-transparent border-none"
          >
            <item.icon
              className={`w-14 h-14 ${
                item.label === activeLabel ? "text-black" : "text-[#b3b3b3]"
              }`}
            />
            <span
              className={`font-['Koulen'] text-xl ${
                item.label === activeLabel ? "text-black" : "text-[#b3b3b3]"
              }`}
            >
              {item.label}
            </span>
          </button>
        ))}
      </div>
    </nav>
  );
};

export default NaviBar;
