--
-- PostgreSQL database dump
--

\restrict Kt8BWaZ3KswJFyhRu3vLfJPPNvce3ci4zuhkUJ29pDRJcZcgWUl6iSIISyouU0b

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 14.19 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: our_warehouse_stocks; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.our_warehouse_stocks (
    id integer NOT NULL,
    variation_id integer NOT NULL,
    unpacked_quantity integer,
    packed_quantity integer,
    updated_at timestamp without time zone
);


ALTER TABLE public.our_warehouse_stocks OWNER TO andrejcernysov;

--
-- Name: our_warehouse_stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.our_warehouse_stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.our_warehouse_stocks_id_seq OWNER TO andrejcernysov;

--
-- Name: our_warehouse_stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.our_warehouse_stocks_id_seq OWNED BY public.our_warehouse_stocks.id;


--
-- Name: ozon_fbo_stocks; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.ozon_fbo_stocks (
    id integer NOT NULL,
    variation_id integer NOT NULL,
    cluster_id integer,
    warehouse_id integer,
    available_stock_count integer,
    valid_stock_count integer,
    transit_stock_count integer,
    reserved_amount integer,
    turnover_grade character varying(50),
    updated_at timestamp without time zone
);


ALTER TABLE public.ozon_fbo_stocks OWNER TO andrejcernysov;

--
-- Name: ozon_fbo_stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.ozon_fbo_stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ozon_fbo_stocks_id_seq OWNER TO andrejcernysov;

--
-- Name: ozon_fbo_stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.ozon_fbo_stocks_id_seq OWNED BY public.ozon_fbo_stocks.id;


--
-- Name: product_categories; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.product_categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.product_categories OWNER TO andrejcernysov;

--
-- Name: product_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.product_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_categories_id_seq OWNER TO andrejcernysov;

--
-- Name: product_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.product_categories_id_seq OWNED BY public.product_categories.id;


--
-- Name: product_variations; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.product_variations (
    id integer NOT NULL,
    product_id integer NOT NULL,
    sku character varying(255) NOT NULL,
    size character varying(50),
    color character varying(50),
    package_quantity integer,
    variation_name character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.product_variations OWNER TO andrejcernysov;

--
-- Name: product_variations_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.product_variations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_variations_id_seq OWNER TO andrejcernysov;

--
-- Name: product_variations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.product_variations_id_seq OWNED BY public.product_variations.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    category_id integer,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.products OWNER TO andrejcernysov;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO andrejcernysov;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: shipment_items; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.shipment_items (
    id integer NOT NULL,
    shipment_id integer NOT NULL,
    variation_id integer NOT NULL,
    quantity integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.shipment_items OWNER TO andrejcernysov;

--
-- Name: shipment_items_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.shipment_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shipment_items_id_seq OWNER TO andrejcernysov;

--
-- Name: shipment_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.shipment_items_id_seq OWNED BY public.shipment_items.id;


--
-- Name: shipments; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.shipments (
    id integer NOT NULL,
    shipment_number character varying(100) NOT NULL,
    status character varying(50),
    destination_warehouse_id integer,
    shipment_date timestamp without time zone,
    expected_delivery_date timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.shipments OWNER TO andrejcernysov;

--
-- Name: shipments_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.shipments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shipments_id_seq OWNER TO andrejcernysov;

--
-- Name: shipments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.shipments_id_seq OWNED BY public.shipments.id;


--
-- Name: stock_movements; Type: TABLE; Schema: public; Owner: andrejcernysov
--

CREATE TABLE public.stock_movements (
    id integer NOT NULL,
    variation_id integer NOT NULL,
    movement_type character varying(50) NOT NULL,
    quantity integer NOT NULL,
    comment text,
    created_at timestamp without time zone
);


ALTER TABLE public.stock_movements OWNER TO andrejcernysov;

--
-- Name: stock_movements_id_seq; Type: SEQUENCE; Schema: public; Owner: andrejcernysov
--

CREATE SEQUENCE public.stock_movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stock_movements_id_seq OWNER TO andrejcernysov;

--
-- Name: stock_movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: andrejcernysov
--

ALTER SEQUENCE public.stock_movements_id_seq OWNED BY public.stock_movements.id;


--
-- Name: our_warehouse_stocks id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.our_warehouse_stocks ALTER COLUMN id SET DEFAULT nextval('public.our_warehouse_stocks_id_seq'::regclass);


--
-- Name: ozon_fbo_stocks id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.ozon_fbo_stocks ALTER COLUMN id SET DEFAULT nextval('public.ozon_fbo_stocks_id_seq'::regclass);


--
-- Name: product_categories id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_categories ALTER COLUMN id SET DEFAULT nextval('public.product_categories_id_seq'::regclass);


--
-- Name: product_variations id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_variations ALTER COLUMN id SET DEFAULT nextval('public.product_variations_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: shipment_items id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipment_items ALTER COLUMN id SET DEFAULT nextval('public.shipment_items_id_seq'::regclass);


--
-- Name: shipments id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipments ALTER COLUMN id SET DEFAULT nextval('public.shipments_id_seq'::regclass);


--
-- Name: stock_movements id; Type: DEFAULT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.stock_movements ALTER COLUMN id SET DEFAULT nextval('public.stock_movements_id_seq'::regclass);


--
-- Data for Name: our_warehouse_stocks; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.our_warehouse_stocks (id, variation_id, unpacked_quantity, packed_quantity, updated_at) FROM stdin;
4	4	0	0	2025-09-21 13:23:42.044925
5	5	0	0	2025-09-21 13:23:42.045548
6	6	0	0	2025-09-21 13:23:42.04613
7	7	0	0	2025-09-21 13:23:42.046693
2	2	0	50	2025-09-21 14:33:56.301864
1	1	399	101	2025-09-21 18:15:28.954995
3	3	190	30	2025-09-21 18:15:28.955004
8	8	950	50	2025-09-21 18:15:28.955007
9	9	970	30	2025-09-21 18:15:28.955009
10	11	445	15	2025-09-21 20:02:56.398094
11	12	395	15	2025-09-21 20:02:56.398103
12	13	445	15	2025-09-21 20:02:56.398106
13	14	395	15	2025-09-21 20:02:56.398108
14	15	445	15	2025-09-21 20:02:56.39811
15	16	395	15	2025-09-21 20:02:56.398112
16	17	445	15	2025-09-21 20:02:56.398114
17	18	395	15	2025-09-21 20:02:56.398116
\.


--
-- Data for Name: ozon_fbo_stocks; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.ozon_fbo_stocks (id, variation_id, cluster_id, warehouse_id, available_stock_count, valid_stock_count, transit_stock_count, reserved_amount, turnover_grade, updated_at) FROM stdin;
\.


--
-- Data for Name: product_categories; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.product_categories (id, name, description, created_at, updated_at) FROM stdin;
1	Носки	Спортивные и повседневные носки	2025-09-20 06:30:36.419655	2025-09-20 06:30:36.419661
2	Футболки	Мужские и женские футболки	2025-09-20 06:30:36.419662	2025-09-20 06:30:36.419663
\.


--
-- Data for Name: product_variations; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.product_variations (id, product_id, sku, size, color, package_quantity, variation_name, created_at, updated_at) FROM stdin;
1	1	НосВыс/В5059/Черн36-41	36-41	черный	5	Цвет черный, Размер 36-41, 5 шт	2025-09-21 13:23:42.039991	2025-09-21 13:23:42.039996
2	1	НосВыс/10пар/В5059/Черн36-41	36-41	черный	10	Цвет черный, Размер 36-41, 10 шт	2025-09-21 13:23:42.041237	2025-09-21 13:23:42.041239
3	1	НосВыс/15пар/Черн36-41	36-41	черный	15	Цвет черный, Размер 36-41, 15 шт	2025-09-21 13:23:42.04302	2025-09-21 13:23:42.043022
4	1	НосВыс/В5258/Бел36-41	36-41	белый	5	Цвет белый, Размер 36-41, 5 шт	2025-09-21 13:23:42.044005	2025-09-21 13:23:42.044008
5	1	НосВыс/10пар/В5258/Бел/36-41	36-41	белый	10	Цвет белый, Размер 36-41, 10 шт	2025-09-21 13:23:42.044637	2025-09-21 13:23:42.044639
6	1	НосВыс/В5059/Черн41-47	41-47	черный	5	Цвет черный, Размер 41-47, 5 шт	2025-09-21 13:23:42.045289	2025-09-21 13:23:42.045291
7	1	НосВыс/10пар/В5059/Черн41-47	41-47	черный	10	Цвет черный, Размер 41-47, 10 шт	2025-09-21 13:23:42.045899	2025-09-21 13:23:42.045901
8	1	НосВыс/В5258/Бел41-47	41-47	белый	5	Цвет белый, Размер 41-47, 5 шт	2025-09-21 13:23:42.046469	2025-09-21 13:23:42.04647
9	1	НосВыс/10пар/В5258/Бел/41-47	41-47	белый	10	Цвет белый, Размер 41-47, 10 шт	2025-09-21 13:23:42.047105	2025-09-21 13:23:42.047106
11	3	НосКорот/Черн36-41/ 5 пар	36-41	черный	5	Цвет черный, Размер 36-41, 5 шт	2025-09-21 19:51:21.477805	2025-09-21 19:51:21.477822
12	3	НосКорот/Черн36-41/ 10 пар	36-41	черный	10	Цвет черный, Размер 36-41, 10 шт	2025-09-21 19:51:21.480152	2025-09-21 19:51:21.480159
13	3	НосКорот/Черн/41-47/ 5 пар	41-47	черный	5	Цвет черный, Размер 41-47, 5 шт	2025-09-21 19:51:21.484218	2025-09-21 19:51:21.484226
14	3	НосКорот/Черн/41-47/ 10 пар	41-47	черный	10	Цвет черный, Размер 41-47, 10 шт	2025-09-21 19:51:21.487595	2025-09-21 19:51:21.487605
15	3	НосКорот/Бел36-41/ 5 пар	36-41	белый	5	Цвет белый, Размер 36-41, 5 шт	2025-09-21 19:51:21.489893	2025-09-21 19:51:21.4899
16	3	НосКорот/Бел36-41/ 10 пар	36-41	белый	10	Цвет белый, Размер 36-41, 10 шт	2025-09-21 19:51:21.492429	2025-09-21 19:51:21.492439
17	3	НосКорот/Бел/41-47/ 5 пар	41-47	белый	5	Цвет белый, Размер 41-47, 5 шт	2025-09-21 19:51:21.49542	2025-09-21 19:51:21.495431
18	3	НосКорот/Бел/41-47/ 10 пар	41-47	белый	10	Цвет белый, Размер 41-47, 10 шт	2025-09-21 19:51:21.497455	2025-09-21 19:51:21.497459
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.products (id, name, category_id, description, created_at, updated_at) FROM stdin;
1	Носки высокие	1	ержан	2025-09-21 13:23:42.037092	2025-09-21 13:23:42.037099
3	Носки короткие	1		2025-09-21 19:51:21.473976	2025-09-21 19:51:21.473985
\.


--
-- Data for Name: shipment_items; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.shipment_items (id, shipment_id, variation_id, quantity, created_at) FROM stdin;
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.shipments (id, shipment_number, status, destination_warehouse_id, shipment_date, expected_delivery_date, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: stock_movements; Type: TABLE DATA; Schema: public; Owner: andrejcernysov
--

COPY public.stock_movements (id, variation_id, movement_type, quantity, comment, created_at) FROM stdin;
1	2	incoming	500		2025-09-21 14:31:18.789769
2	1	incoming	500		2025-09-21 14:31:37.900266
3	3	incoming	500		2025-09-21 14:31:54.415886
4	2	packed	50	 (упаковано 50 уп. по 10 шт.)	2025-09-21 14:33:56.302301
5	3	packed	20	 (упаковано 20 уп. по 15 шт.)	2025-09-21 14:46:29.949723
6	8	incoming	1000	Приход товара: Носки высокие	2025-09-21 17:01:16.292507
7	9	incoming	1000	Приход товара: Носки высокие	2025-09-21 17:01:16.296018
8	1	packing	101	Упаковка товара: Носки высокие	2025-09-21 18:15:28.957835
9	3	packing	10	Упаковка товара: Носки высокие	2025-09-21 18:15:28.957841
10	8	packing	50	Упаковка товара: Носки высокие	2025-09-21 18:15:28.957843
11	9	packing	30	Упаковка товара: Носки высокие	2025-09-21 18:15:28.957846
12	11	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.709711
13	12	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.714443
14	13	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.718478
15	14	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.722282
16	15	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.726226
17	16	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.729163
18	17	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.732527
19	18	incoming	500	Приход товара: Носки короткие	2025-09-21 19:52:04.735193
20	11	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.15354
21	12	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153554
22	13	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153559
23	14	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153564
24	15	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153568
25	16	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153572
26	17	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153577
27	18	packing	5	Упаковка товара: Носки короткие	2025-09-21 19:53:14.153582
28	11	packing	10	Упаковка товара: Носки короткие (10 уп. по 5 шт.)	2025-09-21 20:02:56.405166
29	12	packing	10	Упаковка товара: Носки короткие (10 уп. по 10 шт.)	2025-09-21 20:02:56.405177
30	13	packing	10	Упаковка товара: Носки короткие (10 уп. по 5 шт.)	2025-09-21 20:02:56.405181
31	14	packing	10	Упаковка товара: Носки короткие (10 уп. по 10 шт.)	2025-09-21 20:02:56.405184
32	15	packing	10	Упаковка товара: Носки короткие (10 уп. по 5 шт.)	2025-09-21 20:02:56.405187
33	16	packing	10	Упаковка товара: Носки короткие (10 уп. по 10 шт.)	2025-09-21 20:02:56.405244
34	17	packing	10	Упаковка товара: Носки короткие (10 уп. по 5 шт.)	2025-09-21 20:02:56.405256
35	18	packing	10	Упаковка товара: Носки короткие (10 уп. по 10 шт.)	2025-09-21 20:02:56.405261
\.


--
-- Name: our_warehouse_stocks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.our_warehouse_stocks_id_seq', 17, true);


--
-- Name: ozon_fbo_stocks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.ozon_fbo_stocks_id_seq', 1, false);


--
-- Name: product_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.product_categories_id_seq', 5, true);


--
-- Name: product_variations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.product_variations_id_seq', 18, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.products_id_seq', 3, true);


--
-- Name: shipment_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.shipment_items_id_seq', 1, false);


--
-- Name: shipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.shipments_id_seq', 1, false);


--
-- Name: stock_movements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: andrejcernysov
--

SELECT pg_catalog.setval('public.stock_movements_id_seq', 35, true);


--
-- Name: shipment_items _shipment_variation_uc; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT _shipment_variation_uc UNIQUE (shipment_id, variation_id);


--
-- Name: ozon_fbo_stocks _variation_cluster_warehouse_uc; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.ozon_fbo_stocks
    ADD CONSTRAINT _variation_cluster_warehouse_uc UNIQUE (variation_id, cluster_id, warehouse_id);


--
-- Name: our_warehouse_stocks our_warehouse_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.our_warehouse_stocks
    ADD CONSTRAINT our_warehouse_stocks_pkey PRIMARY KEY (id);


--
-- Name: our_warehouse_stocks our_warehouse_stocks_variation_id_key; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.our_warehouse_stocks
    ADD CONSTRAINT our_warehouse_stocks_variation_id_key UNIQUE (variation_id);


--
-- Name: ozon_fbo_stocks ozon_fbo_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.ozon_fbo_stocks
    ADD CONSTRAINT ozon_fbo_stocks_pkey PRIMARY KEY (id);


--
-- Name: product_categories product_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_name_key UNIQUE (name);


--
-- Name: product_categories product_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_pkey PRIMARY KEY (id);


--
-- Name: product_variations product_variations_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_variations
    ADD CONSTRAINT product_variations_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: shipment_items shipment_items_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT shipment_items_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_shipment_number_key; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_shipment_number_key UNIQUE (shipment_number);


--
-- Name: stock_movements stock_movements_pkey; Type: CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_pkey PRIMARY KEY (id);


--
-- Name: our_warehouse_stocks our_warehouse_stocks_variation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.our_warehouse_stocks
    ADD CONSTRAINT our_warehouse_stocks_variation_id_fkey FOREIGN KEY (variation_id) REFERENCES public.product_variations(id) ON DELETE CASCADE;


--
-- Name: ozon_fbo_stocks ozon_fbo_stocks_variation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.ozon_fbo_stocks
    ADD CONSTRAINT ozon_fbo_stocks_variation_id_fkey FOREIGN KEY (variation_id) REFERENCES public.product_variations(id) ON DELETE CASCADE;


--
-- Name: product_variations product_variations_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.product_variations
    ADD CONSTRAINT product_variations_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.product_categories(id);


--
-- Name: shipment_items shipment_items_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT shipment_items_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(id) ON DELETE CASCADE;


--
-- Name: shipment_items shipment_items_variation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT shipment_items_variation_id_fkey FOREIGN KEY (variation_id) REFERENCES public.product_variations(id) ON DELETE CASCADE;


--
-- Name: stock_movements stock_movements_variation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: andrejcernysov
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_variation_id_fkey FOREIGN KEY (variation_id) REFERENCES public.product_variations(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Kt8BWaZ3KswJFyhRu3vLfJPPNvce3ci4zuhkUJ29pDRJcZcgWUl6iSIISyouU0b

