# guessing-game 
Database course homework using Flask and MongoDB

Chayapol Chaipongsawalee 6210545947


## Usage

Building project in container using command:

```
docker-compose up -d 
```

game is running in **https://localhost/**

Display web server log using command:

```
docker-compose logs -f --tail 10 web
```

Stop project in container using command:

```
docker-compose down -v 
```

## How to play
1. enter question in the field.
2. guess the letter one by one.
3. count show how many times do your guessing wrong.
4. answer show what do you guess right.
5. after you guess all letters play again button will appear.