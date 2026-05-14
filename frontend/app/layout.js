import "./globals.css";

export const metadata = {
  title: "AI Dashboard",
  description: "Lead intelligence dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
