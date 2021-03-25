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

/* layouts/app.twig */
class __TwigTemplate_3c23adfabf7196f7245845755c3da2ee461512a073e7a45f4ef1be4a1f074f08 extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
            'content' => [$this, 'block_content'],
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<!DOCTYPE html>

<meta charset=\"utf-8\">
<meta name=\"description\" content=\"";
        // line 4
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('config')->getCallable(), ["meta_description"]), "html", null, true);
        echo "\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">

<link rel=\"icon\" href=\"";
        // line 7
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('asset')->getCallable(), ["images/favicon.light.png"]), "html", null, true);
        echo "\">
<link rel=\"dns-prefetch\" href=\"//fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\">
<link rel=\"stylesheet\" href=\"";
        // line 10
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('asset')->getCallable(), ["app.css"]), "html", null, true);
        echo "\">

";
        // line 12
        if (call_user_func_array($this->env->getFunction('config')->getCallable(), ["google_analytics_id", false])) {
            // line 13
            echo "    ";
            $this->loadTemplate("components/analytics/google.twig", "layouts/app.twig", 13)->display($context);
        }
        // line 15
        echo "
";
        // line 16
        if ((call_user_func_array($this->env->getFunction('config')->getCallable(), ["matomo_analytics_url", false]) && call_user_func_array($this->env->getFunction('config')->getCallable(), ["matomo_analytics_site_id", false]))) {
            // line 17
            echo "    ";
            $this->loadTemplate("components/analytics/matomo.twig", "layouts/app.twig", 17)->display($context);
        }
        // line 19
        echo "
<title>";
        // line 20
        echo twig_escape_filter($this->env, ($context["title"] ?? null), "html", null, true);
        echo " &bull; ";
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('config')->getCallable(), ["site_title"]), "html", null, true);
        echo "</title>

<div id=\"app\" v-bind:class=\"{ dark: darkMode }\">
    <div class=\"flex flex-col min-h-screen font-sans dark:bg-gray-800\">
        ";
        // line 24
        $this->displayBlock('content', $context, $blocks);
        // line 25
        echo "    </div>

    <div class=\"fixed inset-0 flex items-center justify-center bg-gray-600 p-4 z-50\" v-show=\"loading\">
        <i class=\"fas fa-spinner fa-pulse fa-5x text-white\"></i>
    </div>
</div>

<script src=\"";
        // line 32
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('asset')->getCallable(), ["app.js"]), "html", null, true);
        echo "\"></script>
";
    }

    // line 24
    public function block_content($context, array $blocks = [])
    {
        $macros = $this->macros;
    }

    public function getTemplateName()
    {
        return "layouts/app.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  104 => 24,  98 => 32,  89 => 25,  87 => 24,  78 => 20,  75 => 19,  71 => 17,  69 => 16,  66 => 15,  62 => 13,  60 => 12,  55 => 10,  49 => 7,  43 => 4,  38 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "layouts/app.twig", "/var/www/directorylister/app/views/layouts/app.twig");
    }
}
