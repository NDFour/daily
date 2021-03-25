<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* components/search.twig */
class __TwigTemplate_7a03aec22cf0fef66f396066b1b6d06170e4daee91d86ed581513148139633ca extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<form id=\"search\" action=\".\" method=\"get\" class=\"group relative block bg-blue-700 rounded-full shadow-inner dark:bg-purple-800\">
    <input type=\"text\" value=\"";
        // line 2
        echo twig_escape_filter($this->env, ($context["search"] ?? null), "html", null, true);
        echo "\" name=\"search\" placeholder=\"";
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('translate')->getCallable(), ["search"]), "html", null, true);
        echo "...\"
        class=\"bg-transparent placeholder-gray-900 text-white w-full px-10 py-2\"
        ref=\"searchInput\" v-on:focus=\"\$event.target.select()\"
    >

    <div class=\"flex items-center absolute left-0 inset-y-0 ml-2 pointer-events-none\">
        <div class=\"flex justify-center items-center text-gray-900 text-opacity-50 w-6 h-6\">
            <i class=\"fas fa-search fa-fw\"></i>
        </div>
    </div>

    ";
        // line 13
        if (($context["search"] ?? null)) {
            // line 14
            echo "        <div class=\"flex items-center absolute right-0 inset-y-0 mr-2\">
            <a href=\".\"  class=\"flex justify-center items-center rounded-full text-gray-900 text-opacity-50 w-6 h-6 hover:bg-red-700 hover:text-white hover:text-opacity-100 hover:shadow\">
                <i class=\"fas fa-times\"></i>
            </a>
        </div>
    ";
        }
        // line 20
        echo "</form>
";
    }

    public function getTemplateName()
    {
        return "components/search.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  66 => 20,  58 => 14,  56 => 13,  40 => 2,  37 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "components/search.twig", "/var/www/directorylister/app/views/components/search.twig");
    }
}
