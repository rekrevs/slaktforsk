# Släktforskningsdashboard

Dashboarden är en skrivskyddad, mänskligt orienterad vy över projektets
befintliga personakter, relationer, forskningslogg och Wotan-status. Den har
ingen egen faktadatabas.

```bash
npm install
npm run dev
```

`npm run data` bygger om `public/data/project.json` från filerna under
`genealogy/` och `wotan/backlog.json` när dashboarden ligger i huvudprojektet.
Detta körs automatiskt före både utvecklingsservern och produktionsbygget; ett
fristående publiceringsbygge använder den versionssparade datan.

Verifiera med:

```bash
npm test
npm run build
```
