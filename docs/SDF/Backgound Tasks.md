# Background Tasks
Несмотря на то, что в FastAPI присутствует встроенный механизм BackgroundTasks, я решил, что будет намного выгоднее воспользоваться многопоточностью, поскольку это даёт более удобную настройку и контроль, а также упрощает дальнейший перенос, если мы заходим вынести функционал в отдельный сервис.