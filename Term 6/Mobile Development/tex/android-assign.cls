\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{karazin-assign}[2024/02/18 Karazin University Probability Theory Assignment Template]

%% Class and Options
\def\@@ptsize{14pt} % font size
\DeclareOption{9pt}{\def\@@ptsize{9pt}}
\DeclareOption{10pt}{\def\@@ptsize{10pt}}
\DeclareOption{11pt}{\def\@@ptsize{11pt}}
\DeclareOption{12pt}{\def\@@ptsize{12pt}}
\def\@@solutionmode{1} % default as the solution mode
\DeclareOption{solution}{\def\@@solutionmode{1}} % solution mode
\DeclareOption{problem}{\def\@@solutionmode{0}} % problem mode
\def\@twoside{0} % default as oneside
\DeclareOption{oneside}{\def\@twoside{0}} % one-side document
\DeclareOption{twoside}{\def\@twoside{1}} % two-side document
\ProcessOptions\relax
\LoadClass[a4paper,onecolumn,\@@ptsize]{extarticle}

%% Page Settings
\RequirePackage[inner=2.0cm,outer=2.0cm,top=1.2cm,bottom=3.5cm]{geometry}
\newcommand{\firstfooteradditionalheight}{2em} % additional height for footer on the first page
\hfuzz=.5em % disable false positive of overfull \hbox

%% Document Propertities
\global\let\@assignno\@empty
\global\let\@semester\@empty
\global\let\@studentID\@empty
\global\let\@instructor\@empty
\global\let\@duedate\@empty
\global\let\@author\@empty
\global\let\@mainproblem\@empty
\newcommand{\assignno}[1]{\gdef\@assignno{#1}} % Assignment Number
\newcommand{\semester}[1]{\gdef\@semester{#1}} % Semester
\newcommand{\studentID}[1]{\gdef\@studentID{#1}} % Student ID
\newcommand{\instructor}[1]{\gdef\@instructor{#1}} % Instructor
\newcommand{\duedate}[1]{\gdef\@duedate{#1}} % Due Date of the Assignment
\newcommand{\mainproblem}[1]{\gdef\@mainproblem{#1}} % The main problem of the assignment

%% Fonts and Colors
\RequirePackage[T1]{fontenc}
\RequirePackage[usenames,dvipsnames]{xcolor}

%% TikZ Rule
\RequirePackage{tikz}
\usetikzlibrary{fadings, calc}
\newcommand{\tikzrule}[3][]{\tikz{\fill[#1] (0,0) rectangle (#2,#3);}}

%% Sections Settings
\RequirePackage[explicit]{titlesec} % explained in https://tex.stackexchange.com/a/292307/234654
\RequirePackage{suffix}
% http://mirrors.ctan.org/macros/latex/contrib/titlesec/titlesec.pdf
\pgfdeclarelayer{background}
\pgfsetlayers{background,main}
\global\let\@problempts\@empty
\newcommand{\problempts}[1]{\gdef\@problempts{#1}} % Points of the Problem
\newcommand{\problemptsprint}{\ifx\@problempts\@empty\else(\@problempts~points)\fi}
\newcommand{\sectionheadname}{Задача} % Name for the Section (default as 'Problem')
% Reference: https://tex.stackexchange.com/a/12269/234654
\newcommand{\boxedsection}[4][blue!20]{{%
    \begin{tikzpicture}[inner sep=0pt, inner ysep=0.3ex]
        \node[anchor=base west] at (0,0) (counter) {#2};
        \path let \p1 = (counter.base east) in node[anchor=base west, text width={\textwidth-\x1-#4}] (content)
            at ($(counter.base east)+(#4,0)$) {#3};
        \begin{pgfonlayer}{background}
            \shade[left color=#1,right color=white] let \p1=(counter.north), \p2=(content.north) in
            (0,{max(\y1,\y2)}) rectangle (content.south east);
        \end{pgfonlayer}
    \end{tikzpicture}
}}
% For numbered section, i.e. \section{}
\titleformat{\section}% <command>
    {\Large\bfseries}% <format>
    {}% <label>
    {0pt}% <sep>
    {\boxedsection{\sectionheadname{} \thesection:}{#1}{0.33em}}% <before-code>
    [%
        \vspace{-2.2\baselineskip}\hfill{\normalfont\small\problemptsprint}%
        \problempts{}% clear the problem points
    ]% <after-code>
% For unnumbered section, i.e. \section*{}
\titleformat{name=\section,numberless}% <command>
    {\Large\bfseries}% <format>
    {}% <label>
    {0pt}% <sep>
    {\boxedsection{}{#1}{0em}}% <before-code>
    [%
        \vspace{-2.2\baselineskip}\hfill{\normalfont\small\problemptsprint}%
        \problempts{}% clear the problem points
    ]% <after-code>
\newcommand{\setproblem}[1]{\ifx#1\@empty\else\setcounter{section}{#1}\fi} % force the number of problem
\newcommand{\setsubproblem}[1]{\ifx#1\@empty\else\setcounter{subsection}{#1}\fi} % force the number of subproblem
\newcommand{\problem}[2][]{\problempts{#1}\section[\thesection~#2]{#2}}%
\WithSuffix\newcommand\problem*[2][]{\problempts{#1}\section*{#2}}%
\newcommand{\solutionname}{Solution}%
\newcommand{\startsolution}[1][print]{%
    \setproblem{0}% reset the section counter
    \def\startsolutionprintoption{print}
    \def\startsolutionprintuseroption{#1}
    \ifx\startsolutionprintuseroption\startsolutionprintoption{%
        {%
            \fontfamily{LinuxLibertineT-OsF}\selectfont% select font as Linux Libertine
            \centering\LARGE\scshape%
            \vspace{\baselineskip}%
            \solutionname{}\\[-0.2em]%
        }%
        \noindent%
        \tikzrule[WildStrawberry, path fading=west]{.5\textwidth}{.2em}%
        \tikzrule[WildStrawberry, path fading=east]{.5\textwidth}{.2em}%
    }\fi%
}
\titlespacing*{\section}{0em}{2.5\baselineskip}{1\baselineskip}
\titleformat{\subsection}[runin]{\large\bfseries}{(\arabic{subsection})}{0.33em}{#1}
\newcommand{\subproblem}[1]{\subsection[(\arabic{subsection}) #1]{#1}}
\WithSuffix\newcommand\subproblem*[1]{\subsection*{#1}}
\titleformat{\subsubsection}[runin]{\bfseries}{\arabic{subsubsection}.}{0.33em}{#1}
\newcommand{\subsubproblem}[1]{\subsubsection[\arabic{subsubsection}. #1]{#1}}
\WithSuffix\newcommand\subsubproblem*[1]{\subsubsection*{#1}}

%% Maths Settings
\RequirePackage{mathtools}
\RequirePackage{amssymb}
\RequirePackage{amsthm} % proof environment and others
\RequirePackage{bm} % \bm command
\RequirePackage{nicematrix}
\numberwithin{equation}{section}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}{Proposition}[section]
\newtheorem{lemma}{Lemma}[section]
\newtheorem{corollary}{Corollary}[section]
\newcommand{\hintstyle}{\itshape}
\newcommand{\hint}[1]{({\hintstyle Hint: #1})}
\DeclareMathOperator*{\argmin}{\arg\min}
\DeclareMathOperator*{\argmax}{\arg\max}

%% Code Block Settings
\RequirePackage{listings}
\definecolor{dkgreen}{rgb}{0,0.5,0}
\definecolor{gray}{rgb}{0.5,0.5,0.5}
\definecolor{mauve}{rgb}{0.58,0,0.82}
\lstset{
    numbers=left,  
    frame=tb,
    aboveskip=3mm,
    belowskip=3mm,
    showstringspaces=false,
    columns=fixed,
    framerule=1pt,
    rulecolor=\color{gray!35},
    backgroundcolor=\color{gray!5},
    basicstyle={\ttfamily\small},
    numberstyle=\footnotesize\color{gray},
    keywordstyle=\bfseries\color{MidnightBlue!95!black},
    commentstyle=\color{dkgreen},
    stringstyle=\color{mauve},
    breaklines=true,
    breakatwhitespace=true,
    tabsize=2,
    extendedchars=false,
    postbreak=\mbox{\hspace{-1.4em}\textcolor{purple}{$\hookrightarrow$}\space}
}

%% Captions Settings
\RequirePackage[font=footnotesize,labelfont=bf]{caption}

%% Color Boxes
\RequirePackage[many]{tcolorbox}
\RequirePackage{varwidth}
\newtcolorbox{fancybox}[2][]{enhanced,skin=enhancedlast jigsaw,
    attach boxed title to top left={xshift=-4mm,yshift=-0.5mm},
    fonttitle=\bfseries\sffamily,varwidth boxed title=0.7\linewidth,
    colbacktitle=blue!45!white,colframe=red!50!black,
    interior style={top color=blue!10!white,bottom color=red!10!white},
    boxed title style={empty,arc=0pt,outer arc=0pt,boxrule=0pt},
    underlay boxed title={
        \fill[blue!45!white] (title.north west) -- (title.north east)
        -- +(\tcboxedtitleheight-1mm,-\tcboxedtitleheight+1mm)
        -- ([xshift=4mm,yshift=0.5mm]frame.north east) -- +(0mm,-1mm)
        -- (title.south west) -- cycle;
        \fill[blue!45!white!50!black] ([yshift=-0.5mm]frame.north west)
        -- +(-0.4,0) -- +(0,-0.3) -- cycle;
        \fill[blue!45!white!50!black] ([yshift=-0.5mm]frame.north east)
        -- +(0,-0.3) -- +(0.4,0) -- cycle; },
    title={#2},#1
}
\newtcolorbox{notice}[2][]{enhanced,
    colframe=blue!50!black,colback=blue!10!white,colbacktitle=blue!5!yellow!10!white,
    fonttitle=\bfseries,coltitle=black,attach boxed title to top center=
    {yshift=-0.25mm-\tcboxedtitleheight/2,yshifttext=2mm-\tcboxedtitleheight/2},
    boxed title style={boxrule=0.5mm,
    frame code={ \path[tcb fill frame] ([xshift=-4mm]frame.west)
    -- (frame.north west) -- (frame.north east) -- ([xshift=4mm]frame.east)
    -- (frame.south east) -- (frame.south west) -- cycle; },
    interior code={ \path[tcb fill interior] ([xshift=-2mm]interior.west)
    -- (interior.north west) -- (interior.north east)
    -- ([xshift=2mm]interior.east) -- (interior.south east) -- (interior.south west)
    -- cycle;} },
    title={#2},#1
}

%% Footnote Settings
\RequirePackage[bottom]{footmisc} % glue footnote to bottom
\renewcommand{\footnoterule}{\noindent\tikzrule[SeaGreen, path fading=east]{.4\textwidth}{.1em}}
\renewcommand{\footnotesep}{1em}

%% Header and Footer
\RequirePackage{fancyhdr}
\RequirePackage[colorlinks=true, urlcolor=blue, linkcolor=purple, citecolor=red, hypertexnames=false]{hyperref}
\setlength{\headheight}{52pt}
\setlength{\marginparwidth}{2cm}
\pagestyle{fancy}
\if\@twoside0
    \lhead{
        \fontfamily{LinuxLibertineT-OsF}\selectfont
        \if\@@solutionmode1
            \textsc{\@title~\@assignno} -- \@studentID~\@author
        \else
            \textsc{Probability Theory \@title~\@assignno}
        \fi
    }
    \rhead{\thepage}
    \renewcommand\headrule{\vspace{-0.7em}\tikzrule[BrickRed, path fading=east]{.5\textwidth}{0.3mm}}
\else
    \fancyhf{}
    \renewcommand\headrule{%
        \ifodd\thepage
            \vspace{-0.7em}\tikzrule[BrickRed, path fading=east]{.5\textwidth}{0.3mm}
        \else
            \vspace{-0.7em}\hfill\tikzrule[BrickRed, path fading=west]{.5\textwidth}{0.3mm}
        \fi
    }
    \fancyhead[LO]{
        \fontfamily{LinuxLibertineT-OsF}\selectfont
        \if\@@solutionmode1
            \textsc{\@title~\@assignno} -- \@studentID~\@author
        \else
            \textsc{Probability Theory \@title~\@assignno}
        \fi
        \renewcommand\headrule{\vspace{-0.7em}\tikzrule[BrickRed, path fading=east]{.5\textwidth}{0.3mm}}
    }
    \fancyhead[RE]{
        \fontfamily{LinuxLibertineT-OsF}\selectfont
        \textsc{Probability Theory \@title~\@assignno}
    }
    \fancyhead[LE,RO]{\thepage}
\fi
\cfoot{}
% header and footer style for the first page
\fancypagestyle{firstpage}{
    \renewcommand\headrule{}
    \lhead{}
    \rhead{}
    \cfoot{
        \fontfamily{LinuxLibertineT-OsF}\selectfont
        \vspace*{-\firstfooteradditionalheight}
        \vspace{-1.5em}
        \tikzrule[purple, path fading=west]{.5\textwidth}{.15em}%
        \tikzrule[purple, path fading=east]{.5\textwidth}{.15em}

        \footnotesize\centering
        \if\@@solutionmode1
            Ця \MakeLowercase{\@title{}} строком до \@duedate{}. День здачі роботи -- \@date
        \else
            Ця \MakeLowercase{\@title{}} строком до \textbf{\@duedate{}}
        \fi 
    }
}

%% Title Settings
\RequirePackage{tabularx}
\RequirePackage{afterpage}
\newcommand{\pdftitleadditionalname}{Solution}
\makeatletter         
\renewcommand\maketitle{

    \if\@@solutionmode0
        \ifx\@instructor\@empty
            \let\@instructor\@author % author is the instructor (if not specified)
        \else
            \ifx\@author\@empty
                \let\@author\@instructor % instructor is the author (if not specified)
            \fi
        \fi
    \fi

    \thispagestyle{firstpage}
    \fontfamily{LinuxLibertineT-OsF}\selectfont % set font as Linux Libertine
    \enlargethispage{-\firstfooteradditionalheight} % make room for the footer
    \begin{minipage}{10.5cm}
        \centering
        {
            \fontsize{30}{48}\selectfont
            \textcolor{Plum}{\scshape Розробка на Android}
        }\\[.5em]
        {
            \if\@@solutionmode1
                \@studentID~\@author
                \qquad
            \fi
            \fontsize{12}{48}\textit{Викладач:~\@instructor}
        }
    \end{minipage}
    \begin{minipage}{5cm}
        \vspace{0.7em}
        \centering
        {
            \large
            \fontsize{12}{48}\fontfamily{LinuxBiolinumT-OsF}\selectfont
            \textcolor{BrickRed}{\@semester}
            \vspace{2mm}
        }
        \@title~{\fontfamily{bch}\selectfont\@assignno}
    \end{minipage}
    \\[.3em]
    \tikzrule[cyan, path fading=east]{\textwidth}{.4em}

    \ifx\@mainproblem\@empty
        \vspace{2mm}
    \else
        \begin{center}
            \vspace{-1\baselineskip}\color{RoyalPurple!50!black}
            \LARGE\S~\@mainproblem~\S
        \end{center}
    \fi

    \fontfamily{cmr}\selectfont % Computer Modern

    % Set up document meta data
    % Note that it should be placed here because
    % by now \@author and \@title have been set.
    \hypersetup{
        pdfauthor={\@author},
        pdftitle={%
            \@title~\@assignno~
            \if\@@solutionmode1
                \pdftitleadditionalname{}
            \fi
            - Probability Theory%
        },
        pdfsubject={Probability Theory},
        pdfkeywords={%
            Probability Theory, \@title%
            \ifx\@mainproblem\@empty\else%
                , \@mainproblem%
            \fi%
        },
        pdfcreator={LaTeX with karazin prob class},
        pdfproducer={LaTeX}
    }
}
\makeatother
