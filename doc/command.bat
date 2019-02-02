for /r %%G in (*) do (
   for %%F in (svg) do (
      dot %%G -T%%F -O
   )
)
