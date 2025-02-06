import { useState, useEffect } from "react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { useNavigate } from "react-router-dom";
import NaviBar from "../../components/ui/navigationbar";
import { Search } from "lucide-react";
import { Book } from "../../api/api"
import { dummy_book } from "../../dummy";

const pastelColors = [
  "bg-pink-200", "bg-blue-200", "bg-green-200", "bg-yellow-200", "bg-purple-200", "bg-red-200", "bg-indigo-200"
];

export const Library_home = (): JSX.Element => {
  const navigate = useNavigate();
  const [books, setBooks] = useState<Book[]>([]);
  const [flipped, setFlipped] = useState<{ [key: string]: boolean }>({});
  const [zoomed, setZoomed] = useState<{ [key: string]: boolean }>({});
  
  const dummyBooks = dummy_book;

  useEffect(() => {
    setBooks(dummyBooks);
  }, []);

  return (
    <div className="bg-white flex flex-row justify-center w-full min-h-screen overflow-y-auto relative">
      <div className="bg-white w-[393px] min-h-screen relative pb-16">
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-4xl font-normal text-black text-center">나만의 도서관</h1>
        </div>
        <Separator className="mx-5 mt-8" />
  
        <div className="grid grid-cols-3 gap-0 px-0 mt-0 w-full relative pb-[45px]">
          {books.map((book) => {
            const randomColor = pastelColors[Math.floor(Math.random() * pastelColors.length)];
            return (
              <Card key={book.bookTitle} className="border-none w-full">
                <CardContent className="p-0 flex flex-col items-center">
                  <div
                    className={`relative w-full aspect-[3/4] transform transition-all duration-300 ease-in-out 
                    ${flipped[book.bookTitle] ? "rotate-y-180" : ""} 
                    ${zoomed[book.bookTitle] ? "scale-150 z-50" : "z-10"}`}
                    onClick={() => setFlipped((prev) => ({ ...prev, [book.bookTitle]: !prev[book.bookTitle] }))}
                    onMouseDown={() => setZoomed((prev) => ({ ...prev, [book.bookTitle]: true }))}
                    onMouseUp={() => setZoomed((prev) => ({ ...prev, [book.bookTitle]: false }))}
                  >
                    {/* 앞면: 원래 책 이미지 */}
                    <img
                      className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 
                      ${flipped[book.bookTitle] ? "opacity-0" : "opacity-100"}`}
                      alt="Book cover"
                      src={book.bookimage}
                    />

                    {/* 뒷면: JSX로 직접 생성한 질문 카드 */}
                    <div
                      className={`absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center p-4 rounded-lg shadow-lg transition-opacity duration-500 
                      ${flipped[book.bookTitle] ? "opacity-100" : "opacity-0"} ${randomColor}`}
                    >
                      <div className="w-full h-5 bg-neutral-800 text-white flex items-center justify-center rounded-t-lg text-[7px]">
                        무엇이든 물어보세요!
                      </div>
                      <div className="w-full flex items-center justify-center bg-white text-black p-1 rounded-b-lg text-center text-[10px]">
                        {book.question}
                      </div>
                    </div>

                    {/* 검색 버튼 */}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("/Library_detail", {replace:true});
                      }} 
                      className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 z-50 pointer-events-auto"
                    >
                      <Search className="w-4 h-4 text-gray-600" />
                    </button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
  
        <div className="fixed bottom-0 left-0 w-full bg-white shadow-md z-50">
          <NaviBar activeLabel="Library" />
        </div>
      </div>
    </div>
  );
};
