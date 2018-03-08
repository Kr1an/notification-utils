
--CREATE JOUNRAL TABLE
CREATE TABLE journal (
    activity VARCHAR2(20), 
    event_date DATE, 
    data CLOB
);


-- ACCOUNT LOGGER
CREATE OR REPLACE TRIGGER account_logger
  AFTER 
    INSERT OR 
    UPDATE OF account_id, fullname, password
    OR DELETE 
        ON account
FOR EACH ROW
DECLARE
    log_activity journal.activity%TYPE;
BEGIN
  IF INSERTING THEN
    log_activity := 'Insert';
  ELSIF UPDATING THEN
    log_activity := 'Update';
  ELSIF DELETING THEN
    log_activity := 'Delete';
  END IF;
  
  INSERT INTO journal (activity, event_date, data) VALUES
    (log_activity, SYSDATE, 'account_id: '||:old.account_id||' ---> '||:new.account_id||'; fullname: '||:old.fullname||' ---> '||:new.fullname||'; password: '||:old.password||' ---> '||:new.password||';');
END account_logger;


-- NOTE LOGGER
CREATE OR REPLACE TRIGGER note_logger
  AFTER 
    INSERT OR 
    UPDATE OF note_id, title, modified_date, account_id
    OR DELETE 
        ON note
FOR EACH ROW
DECLARE
    log_activity journal.activity%TYPE;
BEGIN
  IF INSERTING THEN
    log_activity := 'Insert';
  ELSIF UPDATING THEN
    log_activity := 'Update';
  ELSIF DELETING THEN
    log_activity := 'Delete';
  END IF;
  
  INSERT INTO journal (activity, event_date, data) VALUES
    (log_activity, SYSDATE, 'note_id: '||:old.note_id||' ---> '||:new.note_id||'; title: '||:old.title||' ---> '||:new.title||'; modified_date: '||:old.modified_date||' ---> '||:new.modified_date||'; account_id: '||:old.account_id||' ---> '||:new.account_id||';');
END note_logger;


-- ATTACH LOGGER
CREATE OR REPLACE TRIGGER attach_logger
  AFTER 
    INSERT OR 
    UPDATE OF attach_id, path, note_id
    OR DELETE 
        ON attach
FOR EACH ROW
DECLARE
    log_activity journal.activity%TYPE;
BEGIN
  IF INSERTING THEN
    log_activity := 'Insert';
  ELSIF UPDATING THEN
    log_activity := 'Update';
  ELSIF DELETING THEN
    log_activity := 'Delete';
  END IF;
  
  INSERT INTO journal (activity, event_date, data) VALUES
    (log_activity, SYSDATE, 'attach_id: '||:old.attach_id||' ---> '||:new.attach_id||'; path: '||:old.path||' ---> '||:new.path||'; note_id: '||:old.note_id||' ---> '||:new.note_id||';');
END attach_logger;


-- TAG LOGGER
CREATE OR REPLACE TRIGGER tag_logger
  AFTER 
    INSERT OR 
    UPDATE OF tag_id, title
    OR DELETE 
        ON tag
FOR EACH ROW
DECLARE
    log_activity journal.activity%TYPE;
BEGIN
  IF INSERTING THEN
    log_activity := 'Insert';
  ELSIF UPDATING THEN
    log_activity := 'Update';
  ELSIF DELETING THEN
    log_activity := 'Delete';
  END IF;
  
  INSERT INTO journal (activity, event_date, data) VALUES
    (log_activity, SYSDATE, 'tag_id: '||:old.tag_id||' ---> '||:new.tag_id||'; title: '||:old.title||' ---> '||:new.title||';');
END tag_logger;


-- TAG LOGGER
CREATE OR REPLACE TRIGGER tag_note_logger
  AFTER 
    INSERT OR 
    UPDATE OF tag_note_id, tag_link, note_link
    OR DELETE 
        ON tag_note
FOR EACH ROW
DECLARE
    log_activity journal.activity%TYPE;
BEGIN
  IF INSERTING THEN
    log_activity := 'Insert';
  ELSIF UPDATING THEN
    log_activity := 'Update';
  ELSIF DELETING THEN
    log_activity := 'Delete';
  END IF;
  
  INSERT INTO journal (activity, event_date, data) VALUES
    (log_activity, SYSDATE, 'tag_note_id: '||:old.tag_note_id||' ---> '||:new.tag_note_id||'; tag_link: '||:old.tag_link||' ---> '||:new.tag_link||'; note_link: '||:old.note_link||' ---> '||:new.note_link||';');
END tag_note_logger;






