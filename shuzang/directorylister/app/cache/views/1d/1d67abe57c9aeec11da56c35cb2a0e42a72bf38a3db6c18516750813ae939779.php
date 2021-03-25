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

/* error.twig */
class __TwigTemplate_5004e54c07e24ccea31cc5f39c7e001e898c4d868f57cc5baed1dcacec798aa5 extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->blocks = [
            'content' => [$this, 'block_content'],
        ];
    }

    protected function doGetParent(array $context)
    {
        // line 1
        return "layouts/app.twig";
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 2
        $context["title"] = ($context["message"] ?? null);
        // line 1
        $this->parent = $this->loadTemplate("layouts/app.twig", "error.twig", 1);
        $this->parent->display($context, array_merge($this->blocks, $blocks));
    }

    // line 4
    public function block_content($context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 5
        echo "    ";
        $this->loadTemplate("components/header.twig", "error.twig", 5)->display($context);
        // line 6
        echo "
    <div id=\"content\" class=\"flex-grow container flex flex-col justify-center items-center mx-auto px-4 xl:max-w-screen-xl\">
        <p class=\"font-thin text-4xl text-gray-600\">
            ";
        // line 9
        echo twig_escape_filter($this->env, ((array_key_exists("message", $context)) ? (_twig_default_filter(($context["message"] ?? null), "An unexpected error occured")) : ("An unexpected error occured")), "html", null, true);
        echo "
        </p>

        <p class=\"text-lg text-gray-400\">
            ";
        // line 13
        echo twig_escape_filter($this->env, ($context["subtext"] ?? null), "html", null, true);
        echo "
        </p>
    </div>

    ";
        // line 17
        $this->loadTemplate("components/footer.twig", "error.twig", 17)->display($context);
    }

    public function getTemplateName()
    {
        return "error.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  75 => 17,  68 => 13,  61 => 9,  56 => 6,  53 => 5,  49 => 4,  44 => 1,  42 => 2,  35 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "error.twig", "/var/www/directorylister/app/views/error.twig");
    }
}
