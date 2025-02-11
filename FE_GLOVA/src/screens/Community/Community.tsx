import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { HelpCircle } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import NaviBar from "../../components/ui/navigationbar";
import { Book, GetRecommandBooks, GetBooks } from "../../api/api"
import { replace, useNavigate } from "react-router-dom";
import { dummy_book, Nodata } from "../../dummy";
import { cookie_loader, cookie_remover } from "../../api/cookies";


const Page1: React.FC<{ handleBookClick: (book: Book) => void }> = ({ handleBookClick }) => {
    const [search, setSearch] = useState("");
    const carouselRef = useRef<HTMLDivElement>(null);
    let interval = useRef<NodeJS.Timeout | null>(null);
    let isDragging = useRef(false);
    let startX = useRef(0);
    let scrollLeft = useRef(0);

    {/*더미 데이터*/ }
    // const book_data: Book[] = dummy_book

    {/*서버 통신 데이터*/ }
    const [book_data, setBookData] = useState<Book[]>([]);

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const books = await GetRecommandBooks();

                if (books && Array.isArray(books)) {  // ✅ response가 배열인지 체크
                    const transformedBooks = books.map((item: any) => ({
                        recommendationId: item?.recommendation_id || 0,
                        date: item?.date || "0000-00-00",
                        time: item?.time || "00:00:00",
                        bookId: item?.book?.book_id || 0, // ✅ undefined 방지
                        bookTitle: item?.book?.title || "책을 추천받아 보세요!",
                        bookImage: item?.book?.image || "../../image_data/Library_sample.png",
                        questionText: item?.question?.text || "추천 받은 책에 대한 후기를 다른 사람들과 공유할 수 있어요!",
                    }));

                    if (transformedBooks.length > 0) {
                        setBookData(transformedBooks); // ✅ 올바른 변환된 데이터 사용
                    } else {
                        setBookData(Nodata); // ✅ 데이터가 없을 때 더미 데이터 사용
                    }
                } else {
                    setBookData(Nodata); // ✅ API 응답이 배열이 아닐 경우
                }
            } catch (error) {
                console.error("❌ 서버 통신 실패:", error);
                setBookData(Nodata); // ✅ 오류 발생 시 더미 데이터 사용
            }
        };

        fetchBooks();
    }, []);

    useEffect(() => {
        startAutoScroll();
        return () => {
            if (interval.current) clearInterval(interval.current);
        };
    }, []);

    const startAutoScroll = () => {
        if (!carouselRef.current) return;

        interval.current = setInterval(() => {
            if (!isDragging.current && carouselRef.current) {
                carouselRef.current.scrollLeft += 1; // 스크롤 이동

                // 👉 스크롤이 끝에 도달하면 자연스럽게 처음으로 이동
                if (carouselRef.current.scrollLeft >= carouselRef.current.scrollWidth - carouselRef.current.clientWidth) {
                    carouselRef.current.style.scrollBehavior = "auto"; // 애니메이션 OFF
                    carouselRef.current.scrollLeft = 0; // 처음으로 이동
                    carouselRef.current.style.scrollBehavior = "smooth"; // 다시 애니메이션 ON
                }
            }
        }, 20);
    };


    const handleMouseDown = (e: React.MouseEvent) => {
        isDragging.current = true;
        startX.current = e.pageX - (carouselRef.current?.offsetLeft || 0);
        scrollLeft.current = carouselRef.current?.scrollLeft || 0;
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isDragging.current || !carouselRef.current) return;
        const x = e.pageX - carouselRef.current.offsetLeft;
        const walk = (x - startX.current) * 2;
        carouselRef.current.scrollLeft = scrollLeft.current - walk;
    };

    const handleMouseUp = () => {
        isDragging.current = false;
    };

    return (
        <div className="p-4">
            {/* 이미지 슬라이드 */}
            <div
                ref={carouselRef}
                className="flex overflow-x-scroll scroll-smooth space-x-4 p-4 cursor-grab"
                style={{ scrollbarWidth: "none" }}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
            >
                {book_data.map((book, index) => (
                    <motion.div key={index} className="w-[200px] h-[267px] bg-gray-400 flex-shrink-0" whileTap={{ scale: 0.95 }}>
                        <img
                            src={book.bookImage}
                            alt={book.bookTitle}
                            className="w-full h-full object-cover rounded-lg cursor-pointer "
                            onClick={() => handleBookClick(book)}
                        />
                    </motion.div>
                ))}
            </div>


            <hr className="border-t border-2 border-gray-300 my-4" />

            {/* 검색창 */}
            <Input
                type="text"
                placeholder="도서 검색"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="border p-2 w-full "
            />

            <div className="pt-2 w-full text-left font-Freesentation text-xl text-gray-800">
                보유 추천 도서
            </div>


            {/* 동적 Title 리스트 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-2 pb-24">
                {book_data.map((book, index) =>
                    (book.bookTitle.toLowerCase().includes(search.toLowerCase()) || search === "") && (
                        <Card key={index} className="flex justify-between items-end p-2 bg-gray-200 cursor-pointer gap-x-2 relative" onClick={() => handleBookClick(book)}>
                            {/* 왼쪽: 이미지 & 제목 */}
                            <div className="flex items-center gap-x-4">
                                <img className="w-8 h-8 bg-gray-300" src={book.bookImage} alt={book.bookTitle} />
                                <p className="text-[18px] text-gray-600 font-light font-Freesentation" style={{ fontWeight: 300 }}>{book.bookTitle}</p>
                            </div>

                            {/* 오른쪽 하단: 날짜 */}
                            <p className="text-[10px] text-gray-500 absolute bottom-1 right-2">{book.date}</p>
                        </Card>
                    )
                )}
            </div>
        </div>
    );
};

const Page2: React.FC<{ handleBookClick: (book: Book) => void }> = ({ handleBookClick }) => {
    const [search, setSearch] = useState("");
    // const [books, setBooks] = useState<Book[]>([]); // 더미 이미지 (3:4 비율)

    {/*더미 데이터*/ }
    // const books = dummy_book;

    {/*서버 통신 데이터*/ }
    const [books, setBooks] = useState<Book[]>([]);

    useEffect(() => {
        const fetchBooks = async () => {
            const books = await GetBooks();
            setBooks(books);
        };
        fetchBooks();
    }, []);

    return (
        <div className="flex flex-col w-full h-full">
            {/* 검색창 & 전체 검색 문구 */}
            <div className="p-4">
                <h2 className="text-xl font-bold text-left mb-2 font-Freesentation">전체 검색</h2>
                <Input
                    type="text"
                    placeholder="도서 검색"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="border p-2 w-full"
                />
            </div>

            {/* 이미지 리스트 (스크롤 가능) */}
            <div className="flex-1 overflow-y-auto px-4 pb-[108px]">
                <div className="grid grid-cols-3 gap-2">
                    {books.map((book, index) =>
                        (book.bookTitle.toLowerCase().includes(search.toLowerCase()) || search === "") && (
                            <div
                                key={index}
                                className="relative w-full aspect-[3/4] bg-gray-300 flex items-center justify-center text-xs cursor-pointer rounded-lg overflow-hidden"
                                onClick={() => handleBookClick(book)}
                            >
                                {/* 책 이미지 */}
                                <img src={book.bookImage} alt="book image" className="w-full h-full object-cover rounded-lg" />

                                {/* 책 제목 - 최하단 중앙 정렬 */}
                                <p className="absolute bottom-0 w-full bg-black/45 text-white text-center text-sm py-1">
                                    {book.bookTitle}
                                </p>
                            </div>
                        )
                    )}
                </div>
            </div>
        </div>
    );
};



export const Community: React.FC = () => {
    const [page, setPage] = useState(1);
    const navigate = useNavigate(); // ✅ useNavigate()를 컴포넌트 내부에서 선언
    const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);

    useEffect(() => {
        // ✅ 1. 쿠키에서 id 가져오기
        const userIdFromCookie = cookie_loader();

        if (!userIdFromCookie) {
            console.warn("⚠️ 인증 실패! 쿠키가 없음. 로그인 페이지로 이동 (쿠키 생성 실패 또는 쿠키 유효시간 만료)");
            cookie_remover();
            navigate("/", { replace: true });
            return; // 함수 종료
        }

    }, [navigate]);

    const handleBookClick = (book: Book) => {
        navigate("/Review", { replace: true, state: book });
    };

    return (
        <div className="bg-gray-500 flex flex-row justify-center w-full">
            <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
                {/* 상단 아이콘 */}
                <button
                    className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
                    onClick={() => setIsInfoModalOpen(true)}
                >
                    <HelpCircle size={24} />
                </button>

                {/* 페이지 전환 버튼 */}
                <div className="flex justify-center pt-16 px-2 pb-2 gap-x-16">
                    <Button onClick={() => setPage(1)}
                        className={`text-xl font-bold font-Freesentation border-none shadow-none px-4 py-2 rounded-lg bg-white hover:bg-white 
                            ${page === 1 ? "text-green-600" : "text-green-900"}`}>
                        My Books
                    </Button>
                    <Button onClick={() => setPage(2)}
                        className={`text-xl font-bold font-Freesentation border-none shadow-none px-4 py-2 rounded-lg bg-white hover:bg-white 
                            ${page === 2 ? "text-green-600" : "text-green-900"}`}>
                        ALL Books
                    </Button>
                </div>

                <hr className="border-t border-2 border-gray-300" />

                {/* 페이지 렌더링 */}
                {page === 1 ? <Page1 handleBookClick={handleBookClick} /> : <Page2 handleBookClick={handleBookClick} />}

                {/* ✅ 정보 모달 */}
                {isInfoModalOpen && (
                    <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
                        <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
                            <img
                                src="../../image_data/Guide/Commu.png"
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

                {/* NaviBar (고정 하단) */}
                <NaviBar activeLabel="Community" />
            </div>
        </div>

    );
};

