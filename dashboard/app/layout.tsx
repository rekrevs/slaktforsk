import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://slaktarkivet.rekrevs.chatgpt.site'),
  title: 'Släktforskningsöversikt',
  description: 'En levande översikt över släktträdet och det pågående forskningsarbetet.',
  openGraph: {
    title: 'Släktarkivet',
    description: 'Människorna, grenarna och det pågående arbetet',
    images: [{
      url: 'https://slaktarkivet.rekrevs.chatgpt.site/og.png',
      width: 1731,
      height: 909,
      alt: 'Släktarkivet — Människorna, grenarna och det pågående arbetet',
    }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Släktarkivet',
    description: 'Människorna, grenarna och det pågående arbetet',
    images: ['https://slaktarkivet.rekrevs.chatgpt.site/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sv">
      <body>{children}</body>
    </html>
  );
}
