import { useState, useEffect } from "react";
import { HelpCircle } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { useNavigate } from "react-router-dom";
import NaviBar from "../../components/ui/navigationbar";
import { Search } from "lucide-react";
import { Book, GetRecommandBooks } from "../../api/api"
import { dummy_book , Nodata} from "../../dummy";

const pastelColors = [
  "bg-pink-200", "bg-blue-200", "bg-green-200", "bg-yellow-200", "bg-purple-200", "bg-red-200", "bg-indigo-200"
];

export const Library_home = (): JSX.Element => {
  const navigate = useNavigate();
  const [books, setBooks] = useState<Book[]>(Nodata);
  const [flipped, setFlipped] = useState<{ [key: string]: boolean }>({});
  const [zoomed, setZoomed] = useState<{ [key: string]: boolean }>({});
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  
  {/*더미 데이터 버전*/}
  // const dummyBooks = dummy_book;
  // useEffect(() => {
  //   setBooks(dummyBooks);
  // }, []);

  {/*서버 연동 버전*/}
  useEffect(() => {
    const fetchBooks = async () => {
        try {
            const books = await GetRecommandBooks();
            if (books.length > 0) {
              setBooks(books);
            } 
        } catch (error) {
            console.error("서버 통신 실패:", error);
        }
    };
    fetchBooks();
}, []);

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full min-h-screen overflow-y-auto relative">
      <div className="bg-white w-[393px] min-h-screen relative pb-16">
        {/* 상단 아이콘 */}
        <button
          className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
          onClick={() => setIsInfoModalOpen(true)}
        >
          <HelpCircle size={24} />
        </button>

        <div className="inline-flex items-center justify-center w-full mt-[70px]">
        <span className="text-[40px] font-SBAggroB text-black text-center ">나만의 </span>
          <span className="mx-2"> </span>
          <span className="text-[40px] font-SBAggroB text-green-700 text-center ">도서관</span>
        </div>
        <hr className="border-t border-2 border-gray-300 mt-8, mx-4 mb-4" />
  
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
                        무엇이든 얘기해보세요!
                      </div>
                      <div className="w-full flex items-center justify-center bg-white text-black p-1 rounded-b-lg text-center text-[10px]">
                        {book.question}
                      </div>
                    </div>

                    {/* detail 버튼 */}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("/Library_detail", {replace:true, state:book});
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

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img
                src="../../image_data/Guide/Library_home.png" 
                alt="도움말 이미지"
                className="w-full h-auto rounded-md"
              />
              <button
                className="mt-4 px-4 py-2 bg-gray-500 text-white rounded-lg"
                onClick={() => setIsInfoModalOpen(false)}
              >
                닫기
              </button>
            </div>
          </div>
        )}
  
        <div className="fixed bottom-0 left-0 w-full bg-white shadow-md z-50">
          <NaviBar activeLabel="Library" />
        </div>
      </div>
    </div>
  );
};
