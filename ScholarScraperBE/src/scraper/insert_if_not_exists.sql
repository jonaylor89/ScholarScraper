
/*

BEGIN
  UPDATE articles
  SET citation_count = ...
  WHERE id = ...;

  IF sql%rowcount = 0 THEN
    -- no rows were updated, so the record does not exist
    INSERT INTO articles (id, citation_count)
    VALUES ( ... );
  END IF;
END;

*/