<!-- Source: https://pages.graphics.cs.wisc.edu/765-25/posts/evaluating-designs/ -->

# Evaluating Designs: Some thoughts on grading in Posts October 10, 2025 (Last Modified: October 17, 2025)

In assessing student design exercises, we face some of the same challenges as in general visualization evaluation. And there are some additional challenges: we need to be able to assign “absolute” measures (grades) in a consistent way, provide meaningful feedback, and do this at scale…

A good visualization makes its story clear and is clearly effective at telling it. It may use its title, captions, and labels to help guide the viewer to the story and appreciation of the effectiveness of the visual design. It shouldn’t rely on the rationale to explain why the design is effective (although, the rationale is part of the assignments).

These descriptions provide terminology that we will use in evaluation. You will see the *Levels of Correctness* (Bad, Ugly, Good, Splendid) in the assignment. You will see *Types of Designs* and *Aspects of Responses* in our grading. The *Error Codes* are specific things we are looking for. These definitions not only help you understand what we’ve said, but they **give a strong hint for what we will be looking for in assignments.**

## Levels of Correctness

To help think about grading, I take the BUGS framework from the book [Bugs in Writing](https://www.amazon.com/Bugs-Writing-Lyn-Dupre/dp/0201600196). I’ve adapted it a bit.

Aside… My history with this book…

The book is kind of old (it is circa 1995) - and is not one I typically go to (either for myself, or to help students). It is famous for being full of pictures of cats.

My first job after grad school was at Apple. I was in research (they had a research division at the time - they got rid of it in 1997). My lab director (he was my manager’s manager) came in with a big box. He gave all of us (several research groups) a copy of this book, and told us we all needed to learn to write better, and this book was his favorite way to help people learn to write better.

If you want my recommendation for a book that will help you improve your writing, I strongly recommend [Style: Lessons in Clarity and Grace](https://en.wikipedia.org/wiki/Style:_Lessons_in_Clarity_and_Grace).

  - **Bad** - things that are wrong (or, since nothing in Visualization is absolute, unlikely to be right). For example: inappropriate encodings and aggregations (e.g., use of a Tree Map for non-part whole data). Things that are bad can (usually) be clearly identified.
  - **Ugly** - things that aren’t wrong, but are probably not good. Usually these are poor choices (things that are unlikely to be effective). For example: ineffective encodings (e.g., pie charts for comparison between segments). Ugly decisions can often be identified.
  - **Good** - things that make reasonable choices that lead to effective designs.
  - **Splendid** - things that make a particularly clever choice that goes beyond the obvious to do something which is notably effective. (I usually say “superlative”, but the actual book term is splendid)

As we move down this list, it becomes more subjective. Things that are bad are usually clearly breaking some “rule” (to the extent we have rules). The difference between good and splendid is often a matter of taste.

For grading:

  - It is useful to distinguish **Bad** from **Ugly** (and above) - the former should be specifically identifiable, and you should not do them. These “mistakes” will be penalized.
  - There is a subtle distinction between “lack of ugly” and good.

## Types of Designs

For grading, it is useful to distinguish between some categories of design because each has different standards. This isn’t to say that one is better than another, but they have different challenges and ways to excel. Some types of solutions are harder to make than others, so the standards may be different:

1.  **Standard Design (SD)** - A standard design uses a standard chart type for data (and task) that fits it well. Standard designs excel through their use of good design choices (e.g., data selection, scalability strategy) and details to tell their stories well. Details are extremely important - if you’re going to make a standard design, make it well.
      - A special case of this we call **Default Design (DD)** - this is a category of solutions where there is an obvious “standard answer.” Even with a default design, it is feasible to excel through attention to detail.
2.  **Adapted Design (AD)** - Uses a standard design, but in a non-standard way. These designs often make interesting (but still valid) choices in how the data is fit to the design in order to tell a story in an interesting manner.
3.  **Compound Design (CD)** - Uses a combination of simple (usually standard) chart types put together into a single, coherence visualization. Compound designs excel through the choice of the charts so that they work together to tell the story, and the visual details in making the charts work together.
4.  **Non-Standard Design (ND)** - Uses a design that is unlike a basic chart type. These designs require more creativity to invent, and often require care to check their effectiveness. Such designs can excel through their creativity.

## Aspects of Responses

We will be assessing visualizations in the following categories:

  - Question: should be clearly stated, compelling, and sufficiently complex (multi-variate); good questions can be answered with good visualizations (this is a weird definition of good, unique to this assignment). Clarity of the question matters. If we have to guess (or read your rationale) to understand the intent of the visualization, you are unlikely to get full points in this category. Note that this year we are downweighting the “find good questions” (things that are semantically meaningful) aspect - we care that the question you do pick is clear and effectively answered.
  - Answer: does the visualization effectively “answer” the question - does it make the desired things easy to see. This is a holistic assessment of the impression. This is a subjective question of effectiveness. This category does overlap with the others. For example, a poorly chosen design or missing details might make a visualization less effective overall.
  - Design: does the “basic” design choice (e.g., chart type/encoding/layout) support the goals of the visualization. This includes not making “invalid” choices (although, an invalid chart may be ineffective). It also includes scalability and focusing strategies.
  - Details: this includes the details of the design, presentation, and embellishments. Design details include colors. Presentation details include proper formatting such as not showing the UI of the system used to make the visualization. Embellishments include the title, caption, labels, and legends.
  - Rationale: this is a score on what you wrote. Ideally, the visualization speaks for itself - the best assignments can get an A in the other categories before we look at the rationale. But we will grade the rationale as its own thing, and may take it into account in grading other aspects.

## Error Codes

To make giving feedback more efficient and consistent, we establish a set of “codes” - standard things we see in assignments.

For now, we will probably use the list from last year. We will probably create a better organized list (and assign point values to quantify) - but this gets the main ideas across, and gives you a set of things to think about (avoid the bad ones, try to earn the good ones).

[Last Year’s Codes List](https://pages.graphics.cs.wisc.edu/765-24/posts/de5-codes/)
