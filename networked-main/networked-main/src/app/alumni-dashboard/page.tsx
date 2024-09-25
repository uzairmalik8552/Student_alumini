import Image from "next/image";
import AlumniNav from "../Components/AlumniNav";
import AlumniScroller from "../Components/AlumniScroller";
export default function Home() {
  return (
    <div>
      <AlumniNav />
      <AlumniScroller />
    </div>
  );
}
