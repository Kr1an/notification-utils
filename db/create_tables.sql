CREATE TABLE account (
  account_id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  fullname VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  CONSTRAINT account_pk PRIMARY KEY (account_id)
);

CREATE TABLE note (
  note_id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  title VARCHAR(100) NULL,
  text CLOB NULL,
  modified_date DATE NULL,
  account_id NUMBER NOT NULL,
  CONSTRAINT note_pk PRIMARY KEY (note_id),
  CONSTRAINT fk_account
    FOREIGN KEY (account_id)
    REFERENCES account(account_id)
);

CREATE TABLE attach (
  attach_id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  path VARCHAR(300) NULL,
  note_id NUMBER NOT NULL,
  CONSTRAINT attach_pk PRIMARY KEY (attach_id),
  CONSTRAINT fk_note
    FOREIGN KEY (note_id)
    REFERENCES note(note_id)
);

CREATE TABLE tag (
  tag_id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  title VARCHAR(100) NULL,
  CONSTRAINT tag_pk PRIMARY KEY (tag_id)
);

CREATE TABLE tag_note (
  tag_note_id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  tag_link NUMBER NOT NULL,
  note_link NUMBER NOT NULL,
  CONSTRAINT tag_note_pk PRIMARY KEY (tag_note_id),
  CONSTRAINT fk_tag_link
    FOREIGN KEY (tag_link)
    REFERENCES tag(tag_id),
   CONSTRAINT fk_note_link
    FOREIGN KEY (note_link)
    REFERENCES note(note_id) 
);