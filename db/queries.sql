
--auth_query
CREATE OR REPLACE FUNCTION auth (flnm VARCHAR2, pwd VARCHAR2) 
    RETURN NUMBER
IS
    response NUMBER := 0;
BEGIN
    SELECT account_id INTO response FROM account WHERE fullname = flnm AND password = pwd AND ROWNUM = 1;
    RETURN response;
END auth;
/

--create_user
CREATE OR REPLACE FUNCTION create_user (flnm VARCHAR2, pwd VARCHAR2) 
    RETURN NUMBER
IS
    response NUMBER := 0;
BEGIN
    INSERT INTO account (fullname, password) VALUES (flnm, pwd) RETURNING account_id into response;
    RETURN response;
END create_user;
/

--create_tag_query
CREATE OR REPLACE FUNCTION create_tag (tlt VARCHAR2) 
    RETURN NUMBER
IS
    response NUMBER := 0;
BEGIN
    INSERT INTO tag (title) VALUES (tlt) RETURNING tag_id into response;
    RETURN response;
END create_tag;
/

--clear_notes_query
CREATE OR REPLACE PROCEDURE clear_notes (ac_id NUMBER) 
AS
BEGIN
    DELETE FROM note WHERE account_id = ac_id;
END clear_notes;
/

--_get_or_create_tags_query
CREATE OR REPLACE FUNCTION get_tag_by_title (tlt VARCHAR2) 
    RETURN NUMBER
IS
    response NUMBER := 0;
BEGIN
    SELECT tag_id INTO response FROM tag WHERE title = tlt AND ROWNUM = 1;
    RETURN response;
END get_tag_by_title;
/

--_add_tag_note_query
CREATE OR REPLACE PROCEDURE create_tag_note (tg_id NUMBER, n_id NUMBER) 
AS
BEGIN
    INSERT INTO tag_note (tag_link, note_link) VALUES (tg_id, n_id);
END create_tag_note;
/

--_add_files_query
CREATE OR REPLACE PROCEDURE create_attach (pth VARCHAR2, n_id NUMBER) 
AS
BEGIN
    INSERT INTO attach (path, note_id) VALUES (pth, n_id);
END create_attach;
/

--add_note_query
CREATE OR REPLACE PROCEDURE create_note (tlt VARCHAR2, txt CLOB, md DATE, ac_id NUMBER) 
AS
BEGIN
    INSERT INTO note (title, text, modified_date, account_id) VALUES (tlt, txt, md, ac_id);
END create_note;
/

--delete_note_by_id_query
CREATE OR REPLACE PROCEDURE delete_note (ac_id NUMBER, n_id NUMBER) 
AS
BEGIN
    DELETE FROM note WHERE account_id = ac_id AND note_id = n_id;
END delete_note;
/


--update_note_by_id_query
CREATE OR REPLACE PROCEDURE update_note (tlt VARCHAR2, txt CLOB, md DATE, n_id NUMBER, ac_id NUMBER) 
AS
BEGIN
    UPDATE note SET title = tlt, text = txt, modified_date = md WHERE note_id = n_id AND account_id = ac_id;
END update_note;
/

--create_tag_query
-- CREATE TYPE fnote_type AS OBJECT (
-- 	note_id NUMBER,
-- 	note_title VARCHAR2(100),
-- 	text CLOB,
-- 	modified_date DATE,
-- 	tag_title VARCHAR2(100),
-- 	path VARCHAR2(300)
-- );


-- CREATE OR REPLACE FUNCTION get_all_notes (ac_id NUMBER) 
--     RETURN fnote_type
-- IS
--     notes fnote_type := 0;
-- BEGIN
-- 	SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path INTO notes FROM note n LEFT OUTER JOIN file f ON f.note_id=n.note_id LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id WHERE n.account_id=ac_id;
--     RETURN response;
-- END get_all_notes;
-- /
