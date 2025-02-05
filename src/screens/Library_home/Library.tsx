import { useEffect, useState, useRef } from "react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { Vector } from "../../icons/Vector";
import { useNavigate } from "react-router-dom";
import { Server2Books, Book } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";
import { toBlob } from "html-to-image";

const pastelColors = [
  "bg-pink-200", "bg-blue-200", "bg-green-200", "bg-yellow-200", "bg-purple-200", "bg-red-200", "bg-indigo-200"
];

export const Library_home = (): JSX.Element => {
  const navigate = useNavigate();
  const [books, setBooks] = useState<Book[]>([]);
  const [generatedImages, setGeneratedImages] = useState<{ [key: string]: string }>({});
  const [flipped, setFlipped] = useState<{ [key: string]: boolean }>({});
  const [zoomed, setZoomed] = useState<{ [key: string]: boolean }>({});
  const [activeBook, setActiveBook] = useState<string | null>(null);
  const imageRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  const dummyBooks: Book[] = [
    {
      date: "2025-02-06",
      time: "12:30",
      bookTitle: "책 제목 1",
      bookimage: "../../image_data/test1.png",
      question: "이 책은 무엇을 다루고 있을까?",
    },
    {
      date: "2025-02-06",
      time: "14:00",
      bookTitle: "책 제목 2",
      bookimage: "../../image_data/test2.png",
      question: "이야기의 결말은 어떻게 될까?",
    },
    {
      date: "2025-02-06",
      time: "16:45",
      bookTitle: "책 제목 3",
      bookimage: "../../image_data/test3.jpg",
      question: "주인공이 맞닥뜨릴 가장 큰 도전은?",
    },
  ];

  // useEffect(() => {
  //   const getBooks = async () => {
  //     const data = await Server2Books();
  //     setBooks(data);
  //     generateImages(data);
  //   };
  //   getBooks();
  // }, []);


  useEffect(() => {
    setBooks(dummyBooks);
  }, []);

  useEffect(() => {
    if (books.length > 0) {
      generateImages(books);
    }
  }, [books]);

  const generateImages = async (books: Book[]) => {
    const images: { [key: string]: string } = {};
    const containers: HTMLDivElement[] = [];

    books.forEach((book) => {
      const randomColor = pastelColors[Math.floor(Math.random() * pastelColors.length)];
      const container = document.createElement("div");
      container.className = `w-[300px] h-[400px] flex flex-col items-center justify-center p-4 rounded-lg shadow-lg ${randomColor}`;
      container.innerHTML = `
        <div class='w-full h-16 bg-neutral-800 text-white flex items-center justify-center rounded-t-lg'>
          무엇이든 물어보세요!
        </div>
        <div class='w-full flex items-center justify-center bg-white text-black p-4 rounded-b-lg text-center'>
          ${book.question}
        </div>
      `;
      containers.push(container);
      document.body.appendChild(container);
    });

    const imagePromises = containers.map((container) =>
      toBlob(container).then((blob) => URL.createObjectURL(blob))
    );

    const dataUrls = await Promise.all(imagePromises);

    books.forEach((book, index) => {
      images[book.bookTitle] = dataUrls[index];
      document.body.removeChild(containers[index]);
    });

    setGeneratedImages(images);
  };

  const handleBookClick = (book: Book) => {
    setFlipped((prev) => ({ ...prev, [book.bookTitle]: !prev[book.bookTitle] }));
  };

  const handleMouseDown = (book: Book) => {
    setZoomed((prev) => ({ ...prev, [book.bookTitle]: true }));
    setActiveBook(book.bookTitle);
  };

  const handleMouseUp = (book: Book) => {
    setZoomed((prev) => ({ ...prev, [book.bookTitle]: false }));
    setActiveBook(null);
  };

  return (
    <div className="bg-white flex flex-row justify-center w-full h-screen overflow-y-auto">
      <div className="bg-white w-[393px] h-[852px] relative">
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-4xl font-normal text-black text-center">나만의 도서관</h1>
        </div>
        <Separator className="mx-5 mt-8" />

        <div className="grid grid-cols-3 gap-0 px-0 mt-0 w-full relative">
          {books.map((book) => (
            <Card key={book.bookTitle} className="border-none w-full">
              <CardContent className="p-0 flex flex-col items-center">
                <div
                  ref={(el) => (imageRefs.current[book.bookTitle] = el)}
                  className={`relative w-full aspect-[3/4] transform transition-all duration-300 ease-in-out 
                  ${flipped[book.bookTitle] ? "rotate-y-180" : ""} 
                  ${zoomed[book.bookTitle] ? "scale-150 z-50" : "z-10"}`}
                  onClick={() => handleBookClick(book)}
                  onMouseDown={() => handleMouseDown(book)}
                  onMouseUp={() => handleMouseUp(book)}
                >
                  <img
                    className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 
                    ${flipped[book.bookTitle] ? "opacity-0" : "opacity-100"}`}
                    alt="Book cover"
                    src={book.bookimage}
                  />
                  <img
                    className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 
                    ${flipped[book.bookTitle] ? "opacity-100" : "opacity-0"}`}
                    alt="Generated cover"
                    src={generatedImages[book.bookTitle]}
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <NaviBar activeLabel="Library" />
      </div>
    </div>
  );
};
