import { useEffect, useState } from "react";
import { BookOpen, HomeIcon, TimerIcon, TrophyIcon } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { Vector } from "../../icons/Vector";
import { useNavigate } from "react-router-dom";
import { Server2Books, Book } from "../../api/api"; // ✅ API 함수 불러오기

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
  { icon: BookOpen, label: "BOOKS", href: "/Library", active: true },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
];

export const Library_home = (): JSX.Element => {
  const navigate = useNavigate();
  const [books, setBooks] = useState<Book[]>([]); // ✅ 타입 적용

  useEffect(() => {
    const getBooks = async () => {
      const data = await Server2Books(); // ✅ API 호출
      setBooks(data);
    };
    getBooks();
  }, []);

  const handleBookClick = (book: Book) => {
    navigate("../Library_1/Library_1", { state: { book }, replace: true });
  };

  return (
    <div className="bg-white flex flex-row justify-center w-full h-screen overflow-y-auto">
      <div className="bg-white w-[393px] h-[852px] relative">
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-4xl font-normal text-black text-center">나만의 도서관</h1>
        </div>

        <Separator className="mx-5 mt-8" />

        {/* Book List */}
        <div className="grid grid-cols-3 gap-3 px-5 mt-5">
          {books.map((book, index) => (
            <Card key={index} className="border-none">
              <CardContent className="p-2.5 flex flex-col items-center">
                <img
                  className="w-[100px] h-[100px] object-cover cursor-pointer"
                  alt="Book cover"
                  src={book.bookimage}
                  onClick={() => handleBookClick(book)}
                />
                <p className="text-center text-sm mt-2">{book.bookTitle}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Bottom Navigation */}
        <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
          <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
            {navigationItems.map((item) => (
              <button
                key={item.label}
                onClick={() => navigate(item.href, { replace: true })}
                className="flex flex-col items-center w-[82px] h-[75px] bg-transparent border-none"
              >
                <item.icon
                  className={`w-14 h-14 ${item.active ? "text-black" : "text-[#b3b3b3]"}`}
                />
                <span
                  className={`font-['Koulen'] text-xl ${item.active ? "text-black" : "text-[#b3b3b3]"}`}
                >
                  {item.label}
                </span>
              </button>
            ))}
          </div>
        </nav>
      </div>
    </div>
  );
};
