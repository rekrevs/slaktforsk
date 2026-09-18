// T-0660: root authorized minimal revision after independent source comparison.
export const priorHudiksvallFamilyContext = {
  "id": "F-P-0396-family_context-Hudiksvall",
  "version": 1,
  "data": {
    "subject_id": "P-0396",
    "property": "family_context",
    "value_type": "structured",
    "value_json": {
      "cousin_birth_parish_other": "Hudiksvall",
      "cousins": [
        {
          "birth": "1875-09-20",
          "birth_parish": "Alnö",
          "name": "Augusta Fredrika"
        },
        {
          "name": "Hugo"
        },
        {
          "name": "Karl"
        },
        {
          "name": "Esther"
        },
        {
          "name": "Gertrud Elisabet"
        }
      ],
      "other_cousins_birth_year_range": "1882–1891",
      "own_job_is_uncles_or_brothers": false,
      "uncle": "P-0411",
      "uncle_full_or_half_paternal_brother_unresolved": true,
      "uncle_wife": "P-0414"
    }
  }
};
export const hudiksvallFamilyContextRevision = {
  "id": "F-P-0396-family_context-Hudiksvall",
  "kind": "fact",
  "data": {
    "subject_id": "P-0396",
    "property": "family_context",
    "value_type": "structured",
    "value_json": {
      "cousin_birth_parish_other": "Hudiksvall",
      "cousins": [
        {
          "birth_parish": "Alnö",
          "name": "Augusta Fredrika",
          "reported_birth": {
            "C0323": "1875-09-20",
            "C0645": "1875-09-26",
            "chosen": null
          }
        },
        {
          "name": "Hugo"
        },
        {
          "name": "Karl"
        },
        {
          "name": "Esther"
        },
        {
          "name": "Gertrud Elisabet"
        }
      ],
      "other_cousins_birth_year_range": "1882–1891",
      "own_job_is_uncles_or_brothers": false,
      "uncle": "P-0411",
      "uncle_full_or_half_paternal_brother_unresolved": true,
      "uncle_wife": "P-0414"
    }
  },
  "revises": 1,
  "disposition": "accepted",
  "evidenceStatus": "TRANSCRIBED",
  "rationale": "Källjämförelse C0323/C0645; båda datum bevaras och ingen dag väljs. Endast första kusinens födelsedag preciseras.",
  "caveat": "Augusta Fredrikas födelsedag är olöst: Hudiksvall20september,Alnö26september1875. Egen födelsepost ej läst.",
  "origins": [
    "24c950de3b6462b5b71fdfbc5ffc8745b7cb26b3466ea011e9f3405268936ab5",
    "f092a378516c04e184096a3ed4e9683a4cddfcb1a5b6d1715754cfd2974576e5",
    "0301c7f4e33fd061829b99c3d8dc355b149d00acb69dc3049ea5b44ad15f547d",
    "15f5c3ce95618390f7b2f6c584fa18ffcc1592b3833ffc70b00420eab5a9d711",
    {
      "entity": "C-0323",
      "kind": "citation",
      "startLine": 1,
      "endLine": 89
    },
    {
      "entity": "C-0645",
      "kind": "citation",
      "startLine": 1,
      "endLine": 43
    },
    "04c2d203094cd563b4a43233479ee68f9da296eb8f1a495cc72f521753915966"
  ],
  "evidence": [
    {
      "object": "O-P-0411-C0645-Augusta",
      "role": "supports",
      "note": "Alnö sida192,rå75 26/9."
    },
    {
      "object": "O-P-0411-C0323-Augusta",
      "role": "supports",
      "note": "Hudiksvall1875-09-20."
    }
  ]
};
