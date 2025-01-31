--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    question text NOT NULL,
    options jsonb NOT NULL,
    answer text NOT NULL,
    difficulty character varying(50) NOT NULL
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: trivia_questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trivia_questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trivia_questions_id_seq OWNER TO postgres;

--
-- Name: trivia_questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trivia_questions_id_seq OWNED BY public.questions.id;


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.trivia_questions_id_seq'::regclass);


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, question, options, answer, difficulty) FROM stdin;
1	What is the capital of France?	["Berlin", "Madrid", "Paris", "Rome"]	Paris	easy
3	What is 2 + 2?	["3", "4", "5", "6"]	4	easy
7	Who developed the theory of relativity?	["Newton", "Einstein", "Galileo", "Tesla"]	Einstein	hard
2	Who wrote "Romeo and Juliet"?	["Mark Twain", "Charles Dickens", "William Shakespeare", "Jane Austen"]	William Shakespeare	medium
4	What is the capital of India?	["Rajasthan", "Delhi", "Karnataka", "Nepal"]	Delhi	medium
9	Who was the Ancient Greek God of the Sun?	["Zeus", "Athena", "Apollo", "Poseidon"]	Apollo	easy
10	How many minutes are in a full week?	["10,080", "10,000", "10,100", "10,060"]	10,080	hard
11	What company was initially known as "Blue Ribbon Sports"?	["Nike", "Adidas", "Fila", "Reebok"]	Nike	medium
12	What art form is described as "decorative handwriting or handwritten lettering"?	["Graffiti", "Cursive", "Italic Neat", "Calligraphy"]	Calligraphy	medium
13	What city is known as "The Eternal City"?	["Irelad", "Rome", "Paris", "Germany"]	Rome	easy
14	On which continent would you find the world’s largest desert?	["Africa", "Antarctica", "Sahara", "Kalahari"]	Antarctica	easy
15	Which is the only body part that is fully grown from birth?	["Ears", "Tongue", "Eyes", "Teeth"]	Eyes	medium
16	How many colors are there in the rainbow?	["7", "8", "6", "5"]	7	easy
17	What’s a shape with five sides called?	["Octagon", "Pentagon", "Hexagon", "Nonagon"]	Pentagon	easy
6	What is the square root of 144?	["10", "12", "14", "16"]	12	easy
5	What is 5 * 5?	["15", "20", "25", "30"]	25	easy
8	Which country has the highest life expectancy?	["China", "Hong Kong", "India", "America"]	Hong Kong	hard
18	What is the highest-grossing Broadway show of all time?	["Hamilton", "Alladin", "The Lion King", "Harry Potter"]	The Lion King	hard
19	What element does the chemical symbol Au stand for?	["Gold", "Silver", "Platinum", "Aluminum"]	Gold	medium
20	What river runs through Paris?	["Seine", "Loire", "Marne", "Vienne"]	Seine	hard
21	How many continents are there on Earth?	["7", "8", "6", "5"]	7	easy
22	The Statue of Liberty was a gift to the U.S. from what country?	["France", "America", "Europe", "Africa"]	France	medium
23	What is the rarest blood type?	["O positive", "A negative", "AB positive", "AB negative"]	AB negative	medium
24	What country has the highest number of citizens over the age of 65?	["China", "Japan", "America", "India"]	Japan	hard
25	In what year did the Titanic sink?	["1912", "1910", "1915", "1917"]	1912	hard
26	Which bird can fly backward?	["Falcon", "Woodpeckers", "Hummingbird", "Finches"]	Hummingbird	hard
27	What is the hardest naturally occurring substance in the world?	["Quartz", "Diamond", "Carbon", "Graphite"]	Diamond	medium
28	What is the only food that does not spoil?	["Vinegar", "Sugar", "Salt", "Honey"]	Honey	hard
29	Which country is both an island and a continent?	["Australia", "Africa", "Japan", "Antarctica"]	Australia	hard
30	Which artist painted "The Starry Night"?	["Leonardo da Vinci", "Vincent van Gogh", "Claude Monet", "Pablo Picasso"]	Vincent van Gogh	medium
\.


--
-- Name: trivia_questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trivia_questions_id_seq', 30, true);


--
-- Name: questions trivia_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT trivia_questions_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

