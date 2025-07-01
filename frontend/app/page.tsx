"use client";

import styles from "./page.module.css";
import Link from "next/link";
import "./globals.css";


export default function Home() {
  return (
    <div className={styles.page}>

      <header className={styles.header}>Find Your Specialist</header>

      <div className={styles.links}>
        <Link href="/chat" className={styles.bigLink}>
          Start chatting
        </Link>

        <p className={styles.authors}>Powered by Crogs Foundation</p>
      </div>

      <Link href="https://github.com/Crogs-Foundation" target="_blank" className={styles.githubLink}>
        Check our GitHub!
      </Link>
    </div>
  );
}
