SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema notification_utils
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema notification_utils
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `notification_utils` DEFAULT CHARACTER SET utf8 ;
USE `notification_utils` ;

-- -----------------------------------------------------
-- Table `notification_utils`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification_utils`.`user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fullname` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `notification_utils`.`note`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification_utils`.`note` (
  `note_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NULL,
  `text` LONGTEXT NULL,
  `modified_date` DATETIME NULL,
  `user_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`note_id`),
  UNIQUE INDEX `note_id_UNIQUE` (`note_id` ASC),
  INDEX `fk_note_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_note_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `notification_utils`.`user` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `notification_utils`.`file`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification_utils`.`file` (
  `file_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `path` VARCHAR(300) NULL,
  `note_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`file_id`),
  INDEX `fk_file_note_idx` (`note_id` ASC),
  CONSTRAINT `fk_file_note`
    FOREIGN KEY (`note_id`)
    REFERENCES `notification_utils`.`note` (`note_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `notification_utils`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification_utils`.`tag` (
  `tag_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NULL,
  PRIMARY KEY (`tag_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `notification_utils`.`tag_note`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification_utils`.`tag_note` (
  `tag_note_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tag_id` INT UNSIGNED NOT NULL,
  `note_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`tag_note_id`),
  INDEX `fk_tag_note_tag_idx` (`tag_id` ASC),
  INDEX `fk_tag_note_note_idx` (`note_id` ASC),
  CONSTRAINT `fk_tag_note_tag`
    FOREIGN KEY (`tag_id`)
    REFERENCES `notification_utils`.`tag` (`tag_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tag_note_note`
    FOREIGN KEY (`note_id`)
    REFERENCES `notification_utils`.`note` (`note_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
